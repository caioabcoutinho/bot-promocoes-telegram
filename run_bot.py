import os
import logging
from functools import wraps
from telethon import TelegramClient, events
from dotenv import load_dotenv
from src.config import API_ID, API_HASH, USER_CHAT_ID
from src.database import (
    add_product,
    add_store,
    delete_product,
    delete_store,
    get_all_products,
    get_recent_promotions,
    set_store_blocked,
    update_target_price,
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def owner_only(handler):
    @wraps(handler)
    async def guarded(event, *args, **kwargs):
        if event.sender_id != USER_CHAT_ID:
            logger.warning("Comando rejeitado para chat não autorizado: %s", event.sender_id)
            return
        return await handler(event, *args, **kwargs)

    return guarded


# Inicia o cliente como Bot (cria o arquivo bot_session.session)
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
@owner_only
async def cmd_start(event):
    texto = (
        "🤖 **Buscador PC Gamer Ativo!**\n\n"
        "Comandos disponíveis:\n"
        "🛒 `/produtos` - Ver alvos cadastrados\n"
        "🔥 `/ofertas` - Ver últimas 10 promoções salvas"
    )
    await event.reply(texto)

@bot.on(events.NewMessage(pattern='/produtos'))
@owner_only
async def cmd_produtos(event):
    prods = get_all_products()
    if not prods:
        await event.reply("Nenhum produto cadastrado.")
        return
        
    msg = "📦 **Produtos Monitorados:**\n\n"
    for p in prods:
        msg += f"• **{p['name']}** (Alvo: R$ {p['target_price']:.2f})\n"
    await event.reply(msg)

@bot.on(events.NewMessage(pattern='/ofertas'))
@owner_only
async def cmd_ofertas(event):
    promos = get_recent_promotions()
    if not promos:
        await event.reply("Nenhuma promoção encontrada ainda.")
        return
        
    msg = "🔥 **Últimas Ofertas Encontradas:**\n\n"
    for p in promos:
        name, price, store, url, coupon, data = p
        data_formatada = f"{data[8:10]}/{data[5:7]} {data[11:16]}"
        texto_cupom = f"🎟️ Cupom: `{coupon}`\n" if coupon else ""
        
        msg += f"**{name}**\n💰 R$ {price:.2f} na {store}\n{texto_cupom}📅 {data_formatada}\n🔗 [Acessar Loja]({url})\n\n"
        
    await event.reply(msg, link_preview=False)

logger.info("Bot de consulta iniciado! Vá no Telegram e mande /start para ele.")

@bot.on(events.NewMessage(pattern=r'/setalvo'))
@owner_only
async def cmd_setalvo(event):
    import re
    # Busca o padrão: /setalvo "Nome" Preço
    match = re.match(r'/setalvo\s+"([^"]+)"\s+(\d+(?:\.\d+)?)', event.raw_text)
    
    if not match:
        await event.reply(
            '⚠️ **Formato incorreto.**\n'
            'Use: `/setalvo "Nome do Produto" preço`\n'
            'Exemplo: `/setalvo "Ryzen 5 7600" 950`'
        )
        return
        
    nome = match.group(1)
    novo_preco = float(match.group(2))
    
    if update_target_price(nome, novo_preco):
        await event.reply(f'✅ Preço-alvo do **{nome}** atualizado para R$ {novo_preco:.2f}!')
    else:
        await event.reply(f'❌ Produto **{nome}** não encontrado. Verifique o nome exato em /produtos.')

@bot.on(events.NewMessage(pattern=r'/addproduto'))
@owner_only
async def cmd_addproduto(event):
    import re
    # Busca o padrão: /addproduto "Nome" "palavras,chave" "palavras,proibidas" preço
    match = re.match(r'/addproduto\s+"([^"]+)"\s+"([^"]+)"\s+"([^"]*)"\s+(\d+(?:\.\d+)?)', event.raw_text)
    
    if not match:
        await event.reply(
            '⚠️ **Formato incorreto.**\n'
            'Use: `/addproduto "Nome" "palavras,chave" "palavras,proibidas" preco_alvo`\n\n'
            'Exemplo (com exclusão):\n`/addproduto "RTX 4070" "rtx 4070,4070 12gb" "ti,super" 3800`\n\n'
            'Exemplo (sem exclusão):\n`/addproduto "B650" "placa mae b650,b650m" "" 900`'
        )
        return
        
    nome = match.group(1)
    keywords = match.group(2)
    exclude_words = match.group(3)
    target_price = float(match.group(4))
    
    # max_price não está sendo ativamente usado nos alertas ainda, vamos definir 20% acima do alvo como padrão
    max_price = target_price * 1.2 
    
    add_product(nome, keywords, exclude_words, target_price, max_price)
    
    msg = (
        f"✅ **Produto Cadastrado!**\n"
        f"📦 {nome}\n"
        f"🎯 Alvo: R$ {target_price:.2f}\n"
        f"🔍 Buscando por: `{keywords}`\n"
        f"🚫 Ignorando: `{exclude_words if exclude_words else 'Nada'}`"
    )
    await event.reply(msg)

@bot.on(events.NewMessage(pattern=r'/delproduto'))
@owner_only
async def cmd_delproduto(event):
    import re
    match = re.match(r'/delproduto\s+"([^"]+)"', event.raw_text)
    
    if not match:
        await event.reply('⚠️ Use o formato: `/delproduto "Nome do Produto"`')
        return
        
    nome = match.group(1)
    if delete_product(nome):
        await event.reply(f'🗑️ Produto **{nome}** removido do monitoramento.')
    else:
        await event.reply(f'❌ Produto **{nome}** não encontrado.')


@bot.on(events.NewMessage(pattern=r'/addloja'))
@owner_only
async def cmd_addloja(event):
    import re

    match = re.match(r'/addloja\s+"([^"]+)"\s+"([^"]*)"\s+"([^"]*)"', event.raw_text)
    if not match:
        await event.reply(
            '⚠️ Use: `/addloja "Nome" "alias1,alias2" "dominio1.com,dominio2.com"`'
        )
        return
    name, aliases, domains = match.groups()
    add_store(name, aliases, domains)
    await event.reply(f"✅ Loja **{name}** cadastrada/atualizada.")


@bot.on(events.NewMessage(pattern=r'/bloqueialoja'))
@owner_only
async def cmd_bloqueialoja(event):
    import re

    match = re.match(r'/bloqueialoja\s+"([^"]+)"', event.raw_text)
    if not match or not set_store_blocked(match.group(1), True):
        await event.reply('❌ Loja não encontrada. Use `/addloja` primeiro.')
        return
    await event.reply(f"🚫 Loja **{match.group(1)}** bloqueada globalmente.")


@bot.on(events.NewMessage(pattern=r'/desbloqueialoja'))
@owner_only
async def cmd_desbloqueialoja(event):
    import re

    match = re.match(r'/desbloqueialoja\s+"([^"]+)"', event.raw_text)
    if not match or not set_store_blocked(match.group(1), False):
        await event.reply('❌ Loja não encontrada.')
        return
    await event.reply(f"✅ Loja **{match.group(1)}** desbloqueada.")


@bot.on(events.NewMessage(pattern=r'/delloja'))
@owner_only
async def cmd_delloja(event):
    import re

    match = re.match(r'/delloja\s+"([^"]+)"', event.raw_text)
    if not match or not delete_store(match.group(1)):
        await event.reply('❌ Loja não encontrada.')
        return
    await event.reply(f"🗑️ Loja **{match.group(1)}** removida.")

bot.run_until_disconnected()
