# Bot Promoções Telegram

Bot self-hosted para monitorar promoções em grupos e canais do Telegram por
palavras-chave e enviar alertas para o proprietário.

## Como funciona

- Uma conta de usuário do Telegram lê os grupos/canais configurados.
- Um bot do Telegram recebe comandos e envia alertas.
- O banco SQLite e as sessões ficam somente na máquina da instalação.
- Uma instalação possui um único proprietário.

O projeto não calcula frete, cashback ou desconto de cupom. Cupons são exibidos
como informação. Preços no formato `R$ 200,00 x 10` são interpretados como
`R$ 2.000,00`; quando há preço à vista, ele tem prioridade.

## Requisitos

- Python 3.11 ou superior
- Uma conta do Telegram com acesso aos grupos/canais
- Um bot criado pelo [@BotFather](https://t.me/BotFather)
- `API_ID` e `API_HASH` obtidos em <https://my.telegram.org>

## Instalação

### Linux/macOS

```bash
git clone https://github.com/caioabcoutinho/bot-promocoes-telegram.git
cd bot-promocoes-telegram
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

### Windows PowerShell

```powershell
git clone https://github.com/caioabcoutinho/bot-promocoes-telegram.git
cd bot-promocoes-telegram
py -3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha `.env`:

- `API_ID` e `API_HASH`: credenciais da conta de usuário.
- `CHANNELS`: usernames dos grupos/canais separados por vírgula.
- `BOT_TOKEN`: token do bot criado no BotFather.
- `USER_CHAT_ID`: seu ID numérico no Telegram.

Na primeira execução, o Telethon solicitará telefone, código e, se ativado,
senha de 2FA. Isso criará `user_session.session`. O bot usa uma sessão separada.
Nunca publique `.env` ou arquivos `.session`.

## Execução manual

### Entrada recomendada

Use o supervisor único para iniciar os dois componentes:

```bash
python run.py
```

O processo inicia o monitor de promoções e o bot de comandos. `Ctrl+C` encerra
ambos de forma coordenada. Em servidores, prefira o serviço do sistema
operacional descrito abaixo.

### Diagnóstico por componente

```bash
python run_phase3.py  # somente leitura dos grupos e alertas
python run_bot.py     # somente comandos e consulta
```

Não execute `run_phase3.py` e `run.py` ao mesmo tempo: isso duplica a captura.
Os scripts `run_phase1.py` e `run_phase2.py` são históricos e não devem ser
usados na operação normal.

## Execução automática

O comando correto depende do sistema operacional. Em todos os casos, mantenha o
diretório do projeto, o `.env`, as sessões e o banco no mesmo usuário da
instalação.

### Linux com systemd (recomendado para servidor)

O repositório inclui
[`pc-promo-monitor.service`](./deploy/systemd/pc-promo-monitor.service), que usa
o supervisor único. O exemplo pressupõe o projeto em
`~/bot-promocoes-telegram`; se estiver em outro caminho, edite `WorkingDirectory` e
`ExecStart` antes de instalar.

```bash
mkdir -p ~/.config/systemd/user
cp deploy/systemd/pc-promo-monitor.service \
  ~/.config/systemd/user/pc-promo-monitor.service
systemctl --user daemon-reload
systemctl --user enable --now pc-promo-monitor.service
systemctl --user status pc-promo-monitor.service
journalctl --user -u pc-promo-monitor.service -f
```

Para o serviço continuar após logout em um servidor:

```bash
loginctl enable-linger "$USER"
```

Comandos úteis:

```bash
systemctl --user start pc-promo-monitor.service
systemctl --user stop pc-promo-monitor.service
systemctl --user restart pc-promo-monitor.service
systemctl --user enable pc-promo-monitor.service
systemctl --user disable pc-promo-monitor.service
systemctl --user status pc-promo-monitor.service
journalctl --user -u pc-promo-monitor.service -f
```

`sudo systemctl enable pc-monitor pc-bot`, `sudo journalctl -u pc-monitor -f`
e `sudo systemctl status pc-monitor pc-bot` só são válidos se você tiver criado
serviços de sistema com exatamente esses nomes. Eles não existem neste
repositório e, por isso, não são os comandos recomendados. O serviço fornecido
é de usuário e usa `systemctl --user`; isso evita executar o Telegram como root.

### Linux com serviços separados (alternativa de diagnóstico)

Se você deliberadamente criar unidades separadas para `run_phase3.py` e
`run_bot.py`, os equivalentes serão:

```bash
sudo systemctl enable --now pc-monitor pc-bot
sudo systemctl status pc-monitor pc-bot
sudo journalctl -u pc-monitor -f
sudo systemctl restart pc-monitor pc-bot
```

Essa alternativa não deve ser combinada com `run.py`.

### macOS

macOS não possui `systemctl`. Para execução persistente, use `launchd`
(`~/Library/LaunchAgents`) ou um gerenciador como `brew services`. Para validar
manualmente:

```bash
source venv/bin/activate
python run.py
```

Para produção, crie um LaunchAgent cujo `ProgramArguments` execute o caminho
absoluto de `venv/bin/python` e `run.py`, defina `WorkingDirectory` para a raiz
do projeto e redirecione `StandardOutPath`/`StandardErrorPath` para arquivos de
log. Após instalar:

```bash
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.caio.promocoes.plist
launchctl print "gui/$(id -u)/com.caio.promocoes"
launchctl kickstart -k "gui/$(id -u)/com.caio.promocoes"
launchctl bootout "gui/$(id -u)/com.caio.promocoes"
```

### Windows

PowerShell não possui `systemctl`. Para uso manual:

```powershell
.\venv\Scripts\Activate.ps1
python run.py
```

Para iniciar com o Windows, use o Agendador de Tarefas: crie uma tarefa “ao
iniciar o computador” ou “ao fazer logon”, defina o diretório inicial como a
raiz do projeto e execute
`C:\caminho\bot-promocoes-telegram\venv\Scripts\python.exe` com argumento
`C:\caminho\bot-promocoes-telegram\run.py`. Marque “reiniciar a tarefa se falhar”.
Os logs devem ser direcionados para arquivos ou consultados pelo histórico do
Agendador.

Não use `sudo` no Windows e não instale o bot como administrador sem necessidade.

## Operação e troubleshooting

```bash
# validar configuração sem iniciar conexão
python -m compileall -q run.py run_bot.py run_phase3.py src

# conferir testes
python -m pytest -q tests

# verificar se processos do supervisor estão vivos (Linux/macOS)
ps -ef | grep -E 'run.py|run_phase3.py|run_bot.py' | grep -v grep
```

Se o serviço iniciar e parar imediatamente, consulte os logs primeiro. Causas
comuns: `.env` ausente/incompleto, caminho incorreto no serviço, dependências
instaladas fora do `venv`, sessão do Telegram expirada ou outro processo já
usando a mesma sessão. Nunca execute duas instâncias com os mesmos arquivos
`.session`.

## Comandos do bot

```text
/produtos
/ofertas
/addproduto "Nome" "palavra1,palavra2" "exclusao1,exclusao2" preco
/setalvo "Nome" preco
/delproduto "Nome"
/addloja "Shopee" "shopee" "shopee.com.br"
/bloqueialoja "Shopee"
/desbloqueialoja "Shopee"
/delloja "Shopee"
```

Somente o `USER_CHAT_ID` configurado pode executar comandos. Lojas bloqueadas
não geram alertas para nenhum produto. Lojas desconhecidas continuam permitidas.

## Testes automatizados

```bash
python -m pytest -q tests
python -m compileall -q run_bot.py run_phase3.py src tests
```

## Dados locais

O banco é criado em `data/monitor.db`. Faça backup desse arquivo antes de
atualizações. A inicialização aplica migrações idempotentes e preserva o histórico.

## Licença

MIT. Consulte [LICENSE](./LICENSE).
