# Reliable Offers Design

## Design goals

Preservar SQLite e Telethon, mas substituir os três runners por um pipeline único
testável. O domínio deve separar decisão de matching, extração, elegibilidade,
deduplicação, persistência e notificação.

## Components

### Configuration and bootstrap

- Validar variáveis obrigatórias no início.
- Centralizar criação do cliente de leitura e do bot.
- Definir caminhos de dados relativos ao projeto/configuráveis.
- Manter sessões e segredos fora do repositório.

### Domain parsing

- `PriceCandidate`: valor, tipo (`cash` ou `installment`), posição e texto de origem.
- Extrator deve priorizar preço à vista e converter parcela x quantidade.
- URL deve ser normalizada para deduplicação, preservando URL exibida.
- Cupom continua campo informativo.

### Store registry

- Registro persistido de loja, aliases e domínios.
- URL tem precedência sobre texto para identificar loja.
- Loja desconhecida é um resultado válido.
- Blocklist global é consultada antes do alerta.

### Matching

- Normalização de caixa, acentos, separadores e espaços.
- Aliases são OR; exclusões impedem o match.
- Retornar todos os produtos correspondentes.

### Offer pipeline

```text
message
  -> normalize/match all products
  -> extract candidates
  -> identify store
  -> reject blocked store
  -> evaluate target price
  -> persist raw match and offer
  -> check 30-minute dedupe
  -> notify and persist delivery result
```

### Persistence and migration

- Adicionar migração versionada ou inicialização idempotente.
- Preservar tabelas e dados atuais.
- Tornar unicidade de promoção compatível com produto + URL.
- Persistir origem (chat id, nome, mensagem id) e tentativa de notificação.

### Telegram commands

- Restringir comandos por `USER_CHAT_ID`.
- Manter comandos de produtos.
- Adicionar comandos de lojas bloqueadas e aliases/domínios.
- Mensagens de erro devem explicar formato e não esconder falhas.

## Decisions

- Não usar IA para identificar loja no MVP; regras determinísticas são auditáveis.
- Não calcular cupom, frete ou cashback.
- Não alertar com preço ambíguo sem candidato verificável.
- Deduplicação é temporal: 30 minutos para produto + URL + preço.

## Migration risks

- URLs existentes são globais; migração precisa resolver colisões antes de criar
  nova restrição.
- O schema atual tem `coupon` criado depois de `timestamp`; consultas devem usar
  nomes, não posição frágil.
- O banco contém histórico real e deve ser copiado antes de migração.

