from aiogram import Bot
from asgiref.sync import sync_to_async
from api.tg_bot.database import *
from api.tg_bot.user_private import *

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

async def getwebdata(bot):
    n = await get_web_data()
    tg_ids_to_delete = []

    
    for el in n:
        data_id = el['id']
        d = el['order_data']
        if isinstance(d, dict):
            parsed_data = d
        else:
            parsed_data = json.loads(d)
        summa = parsed_data["Order"]["info"]["summa"]
        tg_id = parsed_data["Order"]["user"]["tg_id"]
        discount = parsed_data["Order"]["info"]["discount"]

        # Зал
        hall = list(parsed_data["Order"]["info"]["halls"].values())[0]
        hall_name = hall["name"]
        hall_datetime = hall["datetime"]
        hall_hours = hall["hours"]

        # Дополнительно: еда, услуги, товары
        food_items = parsed_data["Order"]["info"]["food"].values()
        service_items = parsed_data["Order"]["info"]["services"].values()
        goods_items = parsed_data["Order"]["info"]["goods"].values()

        # Формируем список доп. позиций
        additional_items = []
        
        for food in food_items:
            food_name = food["name"]
            food_weight = food["weight"]
            food_price = food["price"]
            food_quantity = food["quantity"]
            additional_items.append(f'{food_name} ({food_weight} г.) — {food_price}₽ x {food_quantity}')

        for service in service_items:
            service_name = service["name"]
            service_time = service["time"]
            service_price = service["price"]
            food_quantity = food["quantity"]
            additional_items.append(f'{service_name} ({service_time} мин.) — {service_price}₽ x {food_quantity}')

        for goods in goods_items:
            goods_name = goods["name"]
            goods_volume = goods["weight"]
            goods_price = goods["price"]
            goods_quantity = goods["quantity"]
            additional_items.append(f'{goods_name} ({goods_volume} мл.) — {goods_price}₽ x {goods_quantity}')

        # Формируем сообщение
        additional_items_str = "\n".join(f"{i+1}. {item}" for i, item in enumerate(additional_items))

        message = (
            f'🛒 Ваш заказ\n'
            f'\n'
            f'Выбранный зал: {hall_name}\n'
            f'Дата: {hall_datetime}\n'
            f'Количество часов: {hall_hours}\n'
            f'\n'
            f'Дополнительно:\n'
            f'{additional_items_str}\n'
            f'\n'
            f'💳 Итоговая стоимость: {summa}₽ (скидка {discount}%)'
        )

        # Отправляем сообщение пользователю
        await bot.send_message(chat_id=int(tg_id), text=message, reply_markup=kb.check_order(data_id))

        # Помечаем данные как просмотренные
        await view_web_data(data_id)


    await delete_msgs(tg_ids_to_delete)