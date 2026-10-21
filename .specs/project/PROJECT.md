# PC Promo Monitor

## Vision

Permitir que uma pessoa monitore grupos e canais do Telegram em busca de ofertas
relevantes para seus produtos desejados, recebendo alertas confiáveis e acionáveis
sem precisar acompanhar várias conversas manualmente.

## Usuário e modelo de operação

- Uma instalação self-hosted pertence a um único proprietário.
- A conta de usuário do Telegram lê grupos/canais que o proprietário pode acessar.
- Um bot do Telegram envia alertas e recebe comandos do proprietário.
- Segredos, sessões e banco local pertencem à instalação e não são publicados.

## Objetivos

1. Corrigir o fluxo de captura, extração, persistência e notificação.
2. Reduzir falsos positivos de produto, preço, loja e cupons.
3. Permitir bloquear globalmente lojas indesejadas e cadastrar aliases/domínios.
4. Tornar a instalação reproduzível em Linux, macOS e Windows.
5. Publicar documentação suficiente para que terceiros configurem a própria instalação.

## Não objetivos do MVP

- Painel web.
- Multiusuário em uma mesma instalação.
- Aplicação automática de cupons, frete ou cashback.
- Docker como caminho principal de instalação.

