# Architecture

**Pattern:** monólito de scripts com módulos utilitários compartilhados.

## Fluxo atual

```text
Telegram user session
        |
        v
NewMessage(chats=CHANNELS)
        |
        v
matcher -> database.raw_matches
        |
        v
extractor -> database.promotions
        |
        v
notifier -> Telegram Bot API
```

## Componentes observados

### Captura

`run_phase1.py`, `run_phase2.py` e `run_phase3.py` criam clientes Telethon
independentes e registram handlers equivalentes.

### Matching

`src/matcher.py` compara substrings em minúsculas. A função retorna somente o
primeiro produto que combinar.

### Extração

`src/extractor.py` usa regex para preço, URL e cupom e uma lista fixa para lojas.
`parse_message` retorna quatro valores.

### Persistência

`src/database.py` cria três tabelas: produtos, matches brutos e promoções. A
promoção usa URL globalmente única e não armazena a mensagem de origem na tabela.

### Notificação

`src/notifier.py` envia Markdown via `aiohttp` e não valida o status HTTP nem
persiste tentativa/falha de entrega.

## Inconsistências arquiteturais

- O fluxo de produção depende de escolher manualmente uma fase.
- O bot de consulta não compartilha o loop de captura.
- O parser e os consumidores têm contratos divergentes.
- Configuração, estado e execução não têm uma camada de inicialização única.

