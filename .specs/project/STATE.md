# Project State

**Updated:** 2026-10-21

## Current phase

MVP foundation implemented and published. The local Linux user service is
installed, enabled, persistent across logout, and currently active.

## Confirmed decisions

- MVP sem painel web.
- Uma instalação tem um proprietário.
- Conta de usuário lê Telegram; bot envia alertas.
- Lojas bloqueadas são globais para todos os produtos.
- Loja desconhecida continua permitida e aparece como desconhecida.
- Cupons são informativos; não entram no cálculo do preço.
- Parcelas explícitas são multiplicadas pelo número de parcelas; preço à vista tem prioridade.
- Matching inicial usa aliases em OR com exclusões.
- Repetidas idênticas são suprimidas por 30 minutos.
- Alertas incluem origem do grupo/canal.
- Lojas devem aceitar aliases/domínios configuráveis pelo bot.
- Distribuição principal: Python nativo com venv/pip.

## Observed blockers and risks

- Há segredos locais no `.env`; eles não podem ser publicados e devem ser rotacionados
  se houver qualquer exposição.
- Não existe CI no GitHub para validar pull requests automaticamente.
- Ainda não há testes de integração do Telegram.
- O serviço instalado localmente aponta para o caminho real da máquina; o arquivo
  versionado é um template que precisa ser ajustado ao caminho de cada instalação.

## Next decision

Adicionar CI e testes de integração somente quando o MVP precisar de uma barreira
de regressão maior; em seguida preparar uma rotina de release.

## Published

- Repository: https://github.com/caioabcoutinho/bot-promocoes-telegram
- Default branch: `main`
- License: MIT
- Local commit: será atualizado após esta mudança.
