# Monitor de Promoções

Este contexto define a linguagem do domínio do monitor de promoções do proprietário.

## Linguagem

**Produto monitorado**:
Um item configurado pelo proprietário com palavras-chave e preço-alvo.

**Oferta**:
Uma mensagem capturada que corresponde a um produto monitorado e contém dados de compra relevantes.

**Loja bloqueada**:
Uma loja cadastrada pelo proprietário para não gerar alertas em nenhum produto.

**Loja desconhecida**:
Uma loja que o sistema não conseguiu identificar com confiança; ela não é bloqueada automaticamente.

**Proprietário**:
O usuário responsável por uma instalação self-hosted e pelo recebimento dos alertas.

## Relações

- Um **proprietário** configura um ou mais **produtos monitorados**.
- Um **produto monitorado** pode gerar várias **ofertas**.
- Uma **loja bloqueada** se aplica a todos os **produtos monitorados** da instalação.
- Uma **oferta** pode pertencer a uma **loja desconhecida**.

## Ambiguidades resolvidas

- O filtro de lojas é global, não específico por produto.
- Somente lojas explicitamente bloqueadas são filtradas.
- Ofertas de lojas desconhecidas continuam permitidas e devem ser identificadas como desconhecidas.
