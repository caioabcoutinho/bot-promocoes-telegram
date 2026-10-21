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

## Configuração do Telegram

### Criar o bot de alertas

1. Abra o Telegram e converse com [@BotFather](https://t.me/BotFather).
2. Envie `/newbot`.
3. Escolha o nome exibido e um username terminado em `bot`.
4. Copie o token retornado para `BOT_TOKEN` no `.env`.
5. Nunca publique esse token. Se ele vazar, use `/revoke` no BotFather e atualize
   o `.env`.

### Obter API_ID e API_HASH

1. Acesse <https://my.telegram.org> com sua conta pessoal.
2. Abra **API development tools**.
3. Crie uma aplicação, se ainda não existir.
4. Copie `api_id` para `API_ID` e `api_hash` para `API_HASH`.

Essas credenciais são da sua conta de usuário, usada para ler os grupos/canais.
O bot criado no BotFather é usado para comandos e alertas; ele não substitui a
conta de usuário para ler grupos privados.

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

`CHANNELS` é obrigatório. Informe os usernames dos grupos/canais que você quer
monitorar, separados por vírgula, incluindo o `@`. A conta usada no primeiro
login precisa ser membro desses grupos/canais. Links privados sem username não
podem ser colocados diretamente nessa lista; nesse caso, use o identificador
aceito pelo Telethon depois de entrar no grupo.

Sugestão de canais para promoções de PC gamer, baseada na configuração original
deste projeto:

```dotenv
CHANNELS=@peperaiohardware,@mmpromo,@HardTecPromocoes,@hardwareofertas,@soplacadevideo,@sopromodecpu
```

Exemplo completo, sem valores reais:

```dotenv
API_ID=12345678
API_HASH=seu_api_hash
CHANNELS=@peperaiohardware,@mmpromo,@HardTecPromocoes
BOT_TOKEN=123456:seu_token_do_bot
USER_CHAT_ID=123456789
```

O `USER_CHAT_ID` é o ID numérico do seu chat pessoal com o bot. Envie `/start`
ao bot e use um bot de consulta de ID ou uma ferramenta equivalente para
descobri-lo. O valor deve ser o seu chat privado, pois os comandos são
rejeitados para outros usuários.

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
O monitor recarrega produtos e lojas do SQLite a cada mensagem. Portanto, depois
de usar comandos como `/addproduto` ou `/bloqueialoja`, não é necessário reiniciar
o serviço.

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
# validar os arquivos sem iniciar conexão
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
/reenviar ID_DA_OFERTA
```

### Exemplos de produtos

```text
/addproduto "Ryzen 7 9800X3D" "ryzen 7 9800x3d,9800x3d" "usado,kit,9800x" 3500
/addproduto "RTX 4070 Super" "rtx 4070 super,4070 super,4070s" "usada,ti" 3800
/addproduto "Memória DDR5 32GB" "ddr5 32gb,2x16gb ddr5,memoria ddr5" "" 700
```

Regras:

- O nome é apenas uma identificação para você e deve ficar entre aspas.
- As palavras-chave ficam em uma única string entre aspas e são separadas por
  vírgulas; qualquer uma delas pode ativar o produto.
- As palavras proibidas ficam em outra string entre aspas e também são separadas
  por vírgulas; se uma aparecer, o produto é ignorado.
- O preço-alvo é o maior preço anunciado que deve gerar alerta.
- Use ponto ou vírgula decimal conforme a versão instalada; exemplos simples
  usam números inteiros.

### O que cada comando faz

- `/start`: mostra um resumo dos comandos.
- `/ajuda`: mostra formatos e exemplos detalhados.
- `/produtos`: lista produtos, palavras configuradas e preços-alvo.
- `/addproduto`: cadastra um produto monitorado.
- `/setalvo`: altera somente o preço-alvo de um produto.
- `/delproduto`: remove o produto e seu monitoramento.
- `/ofertas`: mostra ofertas salvas, origem da mensagem e confirmação do alerta.
- `/reenviar ID_DA_OFERTA`: tenta enviar novamente uma oferta cujo alerta falhou.
- `/lojas`: lista lojas permitidas e bloqueadas.
- `/addloja`: cadastra nome, aliases e domínios de uma loja.
- `/bloqueialoja`: impede alertas dessa loja para todos os produtos.
- `/desbloqueialoja`: permite novamente uma loja.
- `/delloja`: remove o cadastro da loja.
- `/status`: mostra contagens de produtos, lojas, ofertas e matches.

Em `/ofertas`, cada item recebe um ID. Use esse número com `/reenviar` quando o
histórico mostrar uma falha detalhada no envio do alerta.

Somente o `USER_CHAT_ID` configurado pode executar comandos. Lojas bloqueadas
não geram alertas para nenhum produto. Lojas desconhecidas continuam permitidas.

## Testes automatizados

```bash
python -m pytest -q tests
python -m compileall -q run.py run_bot.py run_phase3.py src tests
```

## Dados locais

O banco é criado em `data/monitor.db`. Faça backup desse arquivo antes de
atualizações. A inicialização aplica migrações idempotentes e preserva o histórico.

## Teste pós-reinicialização

Depois de configurar o serviço Linux, faça um reboot controlado:

```bash
sudo reboot
```

Após entrar novamente no sistema, aguarde alguns segundos e verifique:

```bash
systemctl --user is-enabled pc-promo-monitor.service
systemctl --user is-active pc-promo-monitor.service
systemctl --user status pc-promo-monitor.service
journalctl --user -u pc-promo-monitor.service -n 80 --no-pager
```

Os dois primeiros comandos devem retornar `enabled` e `active`. O status deve
mostrar `run.py`, `run_phase3.py` e `run_bot.py` no mesmo cgroup. Em seguida,
envie `/status` ao bot e confirme que ele responde.

## Instalador automático

O projeto ainda usa instalação explícita para evitar executar comandos
privilegiados ou assumir onde cada usuário clonará o repositório. Um instalador
automático poderia:

1. detectar o sistema operacional;
2. criar o virtualenv e instalar dependências;
3. validar o `.env`;
4. criar o serviço no caminho real do projeto;
5. habilitar e iniciar o serviço;
6. verificar logs e mostrar instruções.

No Linux, ele também poderia oferecer `loginctl enable-linger` com confirmação.
No macOS, geraria um `LaunchAgent`; no Windows, uma tarefa do Agendador. Esse
instalador deve ser opcional, pois usuários avançados podem preferir configurar
o serviço manualmente.

## Licença

MIT. Consulte [LICENSE](./LICENSE).
