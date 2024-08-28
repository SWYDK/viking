from aiogram import Bot
from asgiref.sync import sync_to_async
from api.tg_bot.database import *
import api.tg_bot.reply as kb
import re

# П
# Регулярное выражение для поиска номера заказа



async def notify_user(bot: Bot):
    n = await get_msgs()
    tg_ids_to_delete = []

    for el in n:
        msg = el['msg']
        if el['tg_id'] == '-4500825826':
            await bot.send_message(chat_id=-4500825826, text=msg)
            tg_ids_to_delete.append(el['tg_id'])
        else:
            await bot.send_message(chat_id=int(el['tg_id']), text=msg)
            tg_ids_to_delete.append(el['tg_id'])

    await delete_msgs(tg_ids_to_delete)