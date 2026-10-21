import logging
from telethon import TelegramClient, events
from src.config import API_ID, API_HASH, CHANNELS
from src.database import init_db, get_all_products, save_raw_match, save_promotion
from src.matcher import find_matching_product
from src.extractor import parse_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

init_db()
PRODUCTS = get_all_products()
logger.info(f"Monitorando {len(PRODUCTS)} produtos. Aguardando ofertas...")

client = TelegramClient('user_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    msg_text = event.message.text
    if not msg_text:
        return

    product_id, product_name = find_matching_product(msg_text, PRODUCTS)
    
    if product_id:
        chat = await event.get_chat()
        channel_name = getattr(chat, 'username', str(chat.id))
        
        # Salva o log bruto (Fase 1)
        save_raw_match(product_id, channel_name, msg_text)
        
        # Extrai os dados estruturados (Fase 2)
        price, url, store, coupon = parse_message(msg_text)
        
        if price and url:
            # Tenta salvar no banco. Se for duplicado, retorna False.
            is_new = save_promotion(product_id, price, store, url, coupon)
            
            if is_new:
                logger.info(f"💰 NOVA PROMOÇÃO: {product_name}!")
                logger.info(f"   Loja: {store} | Preço: R$ {price}")
                logger.info(f"   Link: {url}")
            else:
                logger.info(f"⚠️ Promoção repetida ignorada: {product_name} na {store}")
        else:
            logger.warning(f"🤔 Match encontrado para {product_name}, mas não consegui extrair preço ou link.")

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
