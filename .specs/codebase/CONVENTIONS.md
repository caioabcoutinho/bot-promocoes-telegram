# Code Conventions

## Naming

- Arquivos e funções usam `snake_case`.
- Variáveis e funções são predominantemente descritivas em inglês.
- Mensagens exibidas ao usuário estão em português.

## Code style

- Módulos pequenos, funções livres e SQL direto.
- Logging usa o módulo padrão `logging`.
- Handlers Telethon são `async`.
- Não há tipagem estática consistente, lint ou formatter configurado.

## Error handling

- Banco fecha conexões manualmente.
- Inserções duplicadas são absorvidas e retornam `False` ou nada.
- O notificador captura qualquer exceção e registra uma mensagem genérica.
- Falhas HTTP sem exceção não são tratadas.

## Configuration

- Variáveis são carregadas com `load_dotenv()`.
- O caminho do banco é relativo: `data/monitor.db`.
- Não existe arquivo de exemplo nem validação de configuração.

