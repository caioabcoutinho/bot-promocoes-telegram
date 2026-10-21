# Tech Stack

**Analyzed:** 2026-10-21

## Core

- Linguagem: Python (código compatível com Python moderno; versão mínima ainda não fixada).
- Runtime: processo Python assíncrono.
- Pacote: `pip` via `requirements.txt`.
- Telegram: Telethon 1.34.0.
- Configuração: python-dotenv 1.0.1.

## Backend e persistência

- Integração: Telegram user client para leitura e Telegram Bot API para alertas/comandos.
- Banco: SQLite via `sqlite3`, sem ORM.
- HTTP: aiohttp usado pelo notificador, instalado no ambiente mas ausente no manifesto.

## Testes

- Nenhum framework ou teste automatizado foi encontrado.

## Desenvolvimento

- Não há `README.md`, `.env.example`, CI, empacotamento ou repositório Git neste diretório.

