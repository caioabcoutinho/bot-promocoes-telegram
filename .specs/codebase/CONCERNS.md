# Concerns

## Correctness

1. Parcelas podem ser tratadas como preço total.
2. `run_phase2.py` quebra ao desempacotar o retorno atual do parser.
3. `run_phase1.py` insere produtos de exemplo ao iniciar.
4. O matching retorna apenas o primeiro produto.
5. Identificação por substring pode confundir lojas e palavras.
6. O preço-alvo atualizado não recalcula `max_price`.

## Notification

1. O fluxo de produção não é claramente selecionável entre as fases.
2. O cupom só funciona no `run_phase3.py`; fases anteriores o perdem.
3. Não há filtro de loja.
4. Não há deduplicação temporal.
5. Falhas de entrega não são persistidas nem expostas ao usuário.

## Operations and security

1. Segredos, sessões e banco não tinham exclusões versionadas antes deste
   discovery.
2. Comandos do bot não verificam `USER_CHAT_ID`.
3. Configuração inválida pode virar `API_ID=0` ou lista vazia sem falha clara.
4. Ausência de documentação impede instalação reproduzível.

## Data evolution

O banco já contém 17 produtos, 768 matches brutos e 630 promoções. Alterações de
schema devem ser migradas sem apagar esse histórico.

