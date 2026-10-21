# Concerns

## Correctness

1. O matching usa substrings e pode confundir aliases muito curtos.
2. O preço-alvo atualizado não recalcula `max_price`, que hoje não participa do alerta.

## Notification

1. O supervisor depende de dois processos Telegram independentes.
2. Falhas de entrega são registradas, mas ainda não há comando para reprocessá-las.

## Operations and security

1. Segredos, sessões e banco não tinham exclusões versionadas antes deste
   discovery.
2. Configuração inválida agora falha com diagnóstico, mas ainda não há comando
   de validação separado.

## Data evolution

O banco já contém 17 produtos, 768 matches brutos e 630 promoções. Alterações de
schema devem ser migradas sem apagar esse histórico.
