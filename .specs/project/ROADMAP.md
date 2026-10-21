# Roadmap

## M0 — Descoberta e baseline

- [x] Mapear código, dependências, banco e fluxos atuais.
- [x] Registrar linguagem de domínio e decisões confirmadas.
- [x] Criar especificação aprovada e critérios de aceitação.

## M1 — Núcleo confiável de ofertas

- [x] Unificar o runner de captura em um supervisor único.
- [x] Corrigir parsing de preço à vista e parcelado.
- [x] Melhorar matching, normalização e exclusões.
- [x] Identificar lojas por domínio/aliases e aplicar bloqueio global.
- [x] Persistir origem, mensagem e estado de notificação.
- [x] Suprimir repetidas por 30 minutos.

## M2 — Operação segura e configurável

- [x] Restringir comandos ao proprietário.
- [x] Adicionar comandos para produtos e lojas.
- [x] Tratar falhas do Telegram com logs e estado explícitos.
- [x] Adicionar testes automatizados para extrator, matcher e regras de alerta.

## M3 — Publicação

- [x] Criar documentação de instalação Linux/macOS/Windows.
- [x] Criar `.env.example` sem segredos e instruções de primeiro login.
- [x] Definir licença MIT.
- [x] Inicializar repositório Git, revisar arquivos excluídos e publicar no GitHub.
