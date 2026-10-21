# Structure

## Files

- `run_phase3.py`: captura, extrai, persiste e tenta notificar.
- `run.py`: supervisor que inicia o monitor e o bot de comandos.
- `run_bot.py`: bot de consulta e comandos de produtos.
- `src/config.py`: lê variáveis de ambiente.
- `src/database.py`: schema e operações SQLite.
- `src/matcher.py`: primeiro produto que combina.
- `src/extractor.py`: preço, URL, loja e cupom.
- `src/notifier.py`: envio HTTP ao Telegram.
- `data/monitor.db`: banco local existente.

## Organização

É uma organização por camada técnica, com um supervisor e dois componentes
executáveis. Não há pacote de domínio separado.
