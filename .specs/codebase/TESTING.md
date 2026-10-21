# Testing

## Current state

Nenhum teste automatizado foi encontrado. A validação disponível durante o
discovery foi compilação dos módulos com `venv/bin/python -m compileall`, que passou.

## Required test layers

### Unit

- Parsing de preço brasileiro, preço à vista e parcelas.
- Extração de URL, cupom e loja por domínio/alias.
- Normalização e matching com aliases/exclusões.
- Filtro global de lojas.
- Deduplicação de 30 minutos.

### Integration

- Persistência SQLite, migração do schema existente e associação produto/oferta.
- Handler com mensagem realista, sem depender de uma sessão Telegram.

### Manual/UAT

- Login da conta de usuário com 2FA.
- Leitura de grupo privado.
- Envio pelo bot ao proprietário.
- Comandos rejeitados para outro chat.

## Gate

Antes de publicar: testes unitários, teste de migração sobre uma cópia do banco
existente, `compileall` e instalação limpa a partir da documentação.

