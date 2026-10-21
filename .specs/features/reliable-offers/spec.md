# Reliable Offers Specification

## Problem Statement

O protótipo captura mensagens do Telegram, mas seus fluxos de execução são
divergentes e geram erros em preço, loja, cupom e repetição de alertas. O objetivo
é transformar o protótipo em uma instalação self-hosted confiável e publicável.

## Goals

- [ ] Corrigir o pipeline ponta a ponta de captura até alerta.
- [ ] Interpretar corretamente preço à vista e parcelado.
- [ ] Permitir bloqueio global de lojas e aliases/domínios configuráveis.
- [ ] Reduzir alertas repetidos para uma mesma oferta em 30 minutos.
- [ ] Documentar instalação nativa em Linux, macOS e Windows.

## Out of Scope

| Feature | Reason |
|---|---|
| Painel web | Explicitamente fora do MVP |
| Multiusuário | Uma instalação tem um proprietário |
| Cálculo de cupom/frete/cashback | Cupom é informativo |
| Docker principal | Distribuição nativa é a prioridade |

## User Stories

### P1: Receber oferta confiável ⭐ MVP

Como proprietário, quero receber uma oferta somente quando produto, preço e URL
forem interpretados de forma consistente, para agir sem conferir vários grupos.

**Acceptance Criteria**

1. WHEN uma mensagem contém um alias de produto e não contém exclusão THEN o sistema SHALL processar todos os produtos correspondentes.
2. WHEN o preço está no formato parcela x quantidade THEN o sistema SHALL usar o total multiplicado.
3. WHEN preço à vista e parcelado coexistem THEN o sistema SHALL preferir o preço à vista.
4. WHEN uma loja está bloqueada THEN o sistema SHALL não enviar alerta.
5. WHEN a loja é desconhecida THEN o sistema SHALL permitir o alerta e marcá-la como desconhecida.

**Independent Test:** enviar mensagens representativas ao pipeline sem Telegram e
verificar produto, preço, loja, cupom e decisão de alerta.

### P1: Evitar ruído

Como proprietário, quero receber no máximo um alerta para a mesma oferta durante
30 minutos, mesmo que ela apareça em vários grupos.

**Acceptance Criteria**

1. WHEN produto + URL + preço forem iguais dentro de 30 minutos THEN o sistema SHALL suprimir o segundo alerta.
2. WHEN o preço mudar ou a janela terminar THEN o sistema SHALL permitir novo alerta.
3. WHEN o envio falhar THEN o sistema SHALL registrar a falha explicitamente.

### P1: Operar com segurança

Como proprietário, quero que somente meu chat administre o bot e que meus segredos
não sejam publicados.

**Acceptance Criteria**

1. WHEN outro chat enviar comando administrativo THEN o sistema SHALL rejeitar a ação.
2. WHEN a configuração obrigatória faltar THEN o sistema SHALL falhar com mensagem clara.
3. WHEN o projeto for clonado THEN o usuário SHALL conseguir configurar `.env` e login sem arquivos de sessão versionados.

## Requirement Traceability

| ID | Story | Status |
|---|---|---|
| OFFER-01 | Receber oferta confiável | Pending |
| OFFER-02 | Interpretar parcelamento | Pending |
| OFFER-03 | Filtrar loja global | Pending |
| OFFER-04 | Identificar loja por domínio/alias | Pending |
| DEDUPE-01 | Suprimir repetidas por 30 minutos | Pending |
| OPER-01 | Restringir comandos ao proprietário | Pending |
| OPER-02 | Instalação multiplataforma | Pending |

## Success Criteria

- Mensagens de teste com `R$ 200,00 x 10` nunca geram preço de R$ 200,00.
- Uma rajada de repostagens iguais gera um único alerta em 30 minutos.
- Uma loja bloqueada gera zero alertas para qualquer produto.
- Um clone limpo instala e inicia seguindo a documentação.
