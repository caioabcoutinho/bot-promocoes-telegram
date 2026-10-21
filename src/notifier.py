import asyncio
import os
import aiohttp
import logging
from src.config import BOT_TOKEN, USER_CHAT_ID

logger = logging.getLogger(__name__)

async def send_alert(product_name, price, store, url, coupon=None, source=None):
    if not BOT_TOKEN or not USER_CHAT_ID:
        logger.error("BOT_TOKEN ou USER_CHAT_ID faltando")
        return False, "BOT_TOKEN ou USER_CHAT_ID faltando"

    # Se houver cupom, adiciona a linha no texto
    texto_cupom = f"\n🎟️ **Cupom:** `{coupon}`" if coupon else ""
    texto_origem = f"\n📣 Origem: {source}" if source else ""
    
    message = (
        f"🚨 **ALERTA DE PREÇO: {product_name}**\n\n"
        f"💰 Preço: R$ {price:.2f}\n"
        f"🏪 Loja: {store}{texto_cupom}\n"
        f"{texto_origem}\n"
        f"🔗 [Acessar Oferta]({url})"
    )

    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": USER_CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": False}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                if response.status >= 400:
                    body = await response.text()
                    logger.error(
                        "Telegram rejeitou alerta: status=%s resposta=%s",
                        response.status,
                        body[:500],
                    )
                    return False, f"Telegram HTTP {response.status}: {body[:500]}"
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        logger.error("Erro de rede ao enviar alerta: %s", error)
        return False, f"Erro de rede: {error}"
    return True, None
