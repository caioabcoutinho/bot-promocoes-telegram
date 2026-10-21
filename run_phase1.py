import logging
from telethon import TelegramClient, events
from src.config import API_ID, API_HASH, CHANNELS
from src.database import init_db, add_product, get_all_products, save_raw_match
from src.matcher import find_matching_product

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializa o banco SQLite e cadastra dois produtos de exemplo
init_db()
add_product(
    name="Ryzen 5 7600",
    keywords="ryzen 5 7600,r5 7600,7600 am5",
    exclude_words="7600x,7600g",
    target_price=1000.0,
    max_price=1150.0
)
add_product(
    name="RX 7800 XT",
    keywords="7800 xt,7800xt",
    exclude_words="7700",
    target_price=3500.0,
    max_price=3800.0
)

PRODUCTS = get_all_products()
logger.info(f"Monitorando {len(PRODUCTS)} produtos nos canais: {CHANNELS}")

# Cria o cliente. 'user_session' será o nome do arquivo da sua sessão gerado localmente.
client = TelegramClient('user_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    msg_text = event.message.text
    if not msg_text:
        return

    chat = await event.get_chat()
    channel_name = getattr(chat, 'username', str(chat.id))

    product_id, product_name = find_matching_product(msg_text, PRODUCTS)
    
    if product_id:
        logger.info(f"🔥 MATCH ENCONTRADO! Produto: {product_name} | Canal: {channel_name}")
        save_raw_match(product_id, channel_name, msg_text)

async def main():
    logger.info("Iniciando cliente Telegram...")
    await client.start()
    logger.info("Ouvindo mensagens... (Pressione Ctrl+C para parar)")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
