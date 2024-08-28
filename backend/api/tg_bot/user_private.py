from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import json
from asgiref.sync import sync_to_async
import requests
import api.tg_bot.reply as kb
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import LabeledPrice, PreCheckoutQuery, SuccessfulPayment, ContentType
from aiogram.utils.i18n import gettext as _
from api.tg_bot.classes_functions import Admin
""" from main.models import User, Orders,Order_list

from main.tg_bot.database import (fetch_order_by_id, fetch_orders, count_orders, get_users_status, get_users, get_pos)"""
from api.tg_bot.database import  *
user_private = Router()


""" import uuid

from yookassa import Configuration, Payment

Configuration.account_id = '424569'
Configuration.secret_key = 'live_ngNmNuCPx8krIaY4n4EaGeYSBk1sVUOoH89h7vh9xxw' """


def create(prices,chat_id):
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
            "amount": {
                "value": f"{prices}",
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "capture":True,
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/pizzafresca_bot"
            },
            "metadata": {
                "chat_id": chat_id,
            },
            "description": f"Заказ в PIZZA FRESKA"
        },  idempotence_key)

        
    
    confirmation_url = payment.confirmation.confirmation_url

    return confirmation_url , payment.id

def check(payment_id):
    payment = Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return False
    else:
        return payment.metadata



@user_private.message(CommandStart())
async def start_message(message: Message):
    user_reg = await add_user(message.from_user.id)
    if user_reg:
        await message.answer('⚔️ Премиальные караоке-бани «Viking»\n'
                            '\n'
                            'Наш официальный бот поможет:\n'
                            '\n'
                            '—  Посмотреть цены на залы, товары и услуги\n'
                            '—  Сделать онлайн-бронь\n'
                            '—  Получать напоминания о записях\n'
                            '\n'
                            '📍 Ул. Кутузова 15\n'
                            '\n'
                            'Нажмите «Начать», чтобы открыть приложение!' ,reply_markup=kb.start_menu)
    else:
        await message.answer('⚔️ Премиальные караоке-бани «Viking»\n'
                            '\n'
                            'Наш официальный бот поможет:\n'
                            '\n'
                            '—  Посмотреть цены на залы, товары и услуги\n'
                            '—  Сделать онлайн-бронь\n'
                            '—  Получать напоминания о записях\n'
                            '\n'
                            '📍 Ул. Кутузова 15\n'
                            '\n'
                            'Нажмите «Начать», чтобы открыть приложение!' ,reply_markup=kb.start_menu_for_reg)



@user_private.message(lambda message: message.web_app_data)
async def get_order(message: Message, state: FSMContext):
    data = message.web_app_data.data
    parsed_data = json.loads(data)
    await state.update_data(order_data=data)

    summa = parsed_data["Order"]["info"]["summa"]
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
        service_quantity = service["quantity"]
        additional_items.append(f'{service_name} ({service_time} мин.) — {service_price}₽ x {service_quantity}')

    for goods in goods_items:
        goods_name = goods["name"]
        goods_volume = goods["volume "]
        goods_price = goods["price"]
        goods_quantity = goods["quantity"]
        additional_items.append(f'{goods_name} ({goods_volume} мл.) — {goods_price}₽ x {goods_quantity}')

    # Сообщение
    additional_items_str = "\n".join(f"{i+1}. {item}" for i, item in enumerate(additional_items))

    await message.answer(
        f'🛒 Ваш заказ\n'
        f'\n'
        f'Выбранный зал: {hall_name}\n'
        f'Дата: {hall_datetime}\n'
        f'Количество часов: {hall_hours}\n'
        f'\n'
        f'Дополнительно:\n'
        f'{additional_items_str}\n'
        f'\n'
        f'💳 Итоговая стоимость: {summa}₽ (скидка {discount}%)', reply_markup = kb.check_order()
    )

