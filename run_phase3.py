import logging
from telethon import TelegramClient, events
from src.config import API_ID, API_HASH, CHANNELS
from src.database import (
    get_all_products,
    get_stores,
    init_db,
    is_recent_duplicate,
    save_promotion,
    save_raw_match,
)
from src.matcher import find_matching_products
from src.extractor import identify_store, parse_message
from src.notifier import send_alert

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

init_db()
PRODUCTS = get_all_products()
logger.info("Monitorando produtos. Aguardando ofertas...")

client = TelegramClient('user_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    msg_text = event.message.text
    if not msg_text:
        return

    matches = find_matching_products(msg_text, PRODUCTS)
    if not matches:
        return

    chat = await event.get_chat()
    channel_name = getattr(chat, 'username', str(chat.id))
    chat_id = getattr(chat, 'id', None)
    price, url, _, coupon = parse_message(msg_text)
    store, blocked = identify_store(msg_text, url, get_stores())

    for product_id, product_name in matches:
        save_raw_match(product_id, channel_name, msg_text, chat_id, event.id)
        if blocked or price is None or url is None:
            continue
        product = next(product for product in PRODUCTS if product["id"] == product_id)
        if price > product["target_price"]:
            continue
        if is_recent_duplicate(product_id, price, url):
            logger.info("Oferta repetida suprimida: %s", product_name)
            continue
        if save_promotion(product_id, price, store, url, coupon, chat_id, event.id):
            await send_alert(
                product_name, price, store, url, coupon, channel_name
            )

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
