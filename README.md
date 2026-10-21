# PC Promo Monitor

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
git clone <URL_DO_REPOSITORIO>
cd pc_promo_monitor
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

### Windows PowerShell

```powershell
git clone <URL_DO_REPOSITORIO>
cd pc_promo_monitor
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

## Execução

Em um terminal, execute o monitor:

```bash
python run_phase3.py
```

Em outro terminal, execute o bot de comandos:

```bash
python run_bot.py
```

O nome `run_phase3.py` será substituído por um entrypoint único na próxima etapa
de limpeza do MVP. Não execute `run_phase1.py` junto com `run_phase3.py`, pois
isso duplicará a captura de mensagens.

## Comandos

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

## Testes

```bash
python -m pytest -q tests
python -m compileall -q run_bot.py run_phase3.py src tests
```

## Dados locais

O banco é criado em `data/monitor.db`. Faça backup desse arquivo antes de
atualizações. A inicialização aplica migrações idempotentes e preserva o histórico.

## Licença

MIT. Consulte [LICENSE](./LICENSE).
