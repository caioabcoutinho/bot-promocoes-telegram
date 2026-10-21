import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _integer_env(name):
    value = os.getenv(name, "").strip()
    if not value:
        return 0
    try:
        return int(value)
    except ValueError:
        return 0


API_ID = _integer_env("API_ID")
API_HASH = os.getenv("API_HASH", "")
CHANNELS = [c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()]
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
USER_CHAT_ID = _integer_env("USER_CHAT_ID")
DB_PATH = str(PROJECT_ROOT / "data" / "monitor.db")


def validate_configuration():
    errors = []
    if API_ID <= 0:
        errors.append("API_ID deve ser um número positivo de my.telegram.org")
    if not API_HASH:
        errors.append("API_HASH não informado")
    if not BOT_TOKEN or ":" not in BOT_TOKEN:
        errors.append("BOT_TOKEN inválido ou não informado pelo BotFather")
    if USER_CHAT_ID == 0:
        errors.append("USER_CHAT_ID não informado ou inválido")
    if not CHANNELS:
        errors.append(
            "CHANNELS está vazio; informe os @ dos grupos/canais separados por vírgula"
        )
    if errors:
        raise RuntimeError(
            "Configuração inválida:\n- " + "\n- ".join(errors)
        )
