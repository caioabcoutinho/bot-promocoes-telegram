# Project State

**Updated:** 2026-10-21

## Current phase

Discovery/brownfield mapping. Implementation has not started.

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

- O diretório atual não é um repositório Git.
- Há segredos locais no `.env`; eles não podem ser publicados e devem ser rotacionados
  se houver qualquer exposição.
- Há três scripts de fase com fluxos divergentes; o bot de consulta e o monitor não
  são um único processo.
- `run_phase2.py` desempacota três valores de uma função que retorna quatro.
- `requirements.txt` não declara `aiohttp`, embora o notificador o importe.
- O parser atual pode interpretar parcelas como preço total.
- A URL da promoção é única no banco inteiro, não por produto.

## Next decision

Aprovar a especificação M1 antes de implementar. A licença do projeto ainda está
pendente.

