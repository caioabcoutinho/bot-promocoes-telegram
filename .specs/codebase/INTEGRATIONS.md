# Integrations

## Telegram user API

Telethon usa `API_ID`, `API_HASH`, `CHANNELS` e `user_session.session` para ler
mensagens de grupos/canais acessíveis à conta.

## Telegram Bot API

O bot usa `BOT_TOKEN` para comandos e para enviar alertas a `USER_CHAT_ID`.

## Local filesystem

SQLite é persistido em `data/monitor.db`; sessões Telethon ficam na raiz. Esses
artefatos devem permanecer locais.

## Network and reliability concerns

- Não há timeout, retry ou interpretação de status no POST do notificador.
- Uma sessão e um banco local tornam a operação stateful por instalação.
- Telegram pode rejeitar Markdown malformado ou links inválidos.

