# Structure

## Files

- `run_phase1.py`: captura e persiste matches brutos.
- `run_phase2.py`: captura, extrai oferta e persiste promoção.
- `run_phase3.py`: captura, extrai, persiste e tenta notificar.
- `run_bot.py`: bot de consulta e comandos de produtos.
- `src/config.py`: lê variáveis de ambiente.
- `src/database.py`: schema e operações SQLite.
- `src/matcher.py`: primeiro produto que combina.
- `src/extractor.py`: preço, URL, loja e cupom.
- `src/notifier.py`: envio HTTP ao Telegram.
- `data/monitor.db`: banco local existente.

## Organização

É uma organização por camada técnica, com scripts executáveis separados por fase.
Não há fronteira única de aplicação nem pacote de domínio.

