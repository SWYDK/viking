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
from aiogram import Bot
""" from main.models import User, Orders,Order_list

from main.tg_bot.database import (fetch_order_by_id, fetch_orders, count_orders, get_users_status, get_users, get_pos)"""
from api.tg_bot.database import  *
user_private = Router()
from os import getenv, environ
from dotenv import load_dotenv
from aiogram.methods.get_user_profile_photos import GetUserProfilePhotos
import uuid
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
import aiohttp
import os
from pathlib import Path

from yookassa import Configuration, Payment

Configuration.account_id = '444865'
Configuration.secret_key = 'test_nI8QUkSZ2iv-HYfnk40r37LBxmSZpev44ko2xCsH0Jo' 

load_dotenv()

bot = Bot(getenv('bot_token'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


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
                "return_url": "https://t.me/Vikingrznbot"
            },
            "metadata": {
                "chat_id": chat_id,
            },
            "description": f"Заказ в VIKING"
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
async def start_message(message: Message, bot: Bot):
    UserProfilePhotos = await bot.get_user_profile_photos(user_id=message.from_user.id)
    if UserProfilePhotos.total_count > 0:
        # Извлекаем `file_id` первой фотографии
        first_photo = UserProfilePhotos.photos[0][0]
        file_id = first_photo.file_id
        
        # Сформируем URL для получения фотографии
        file = await bot.get_file(file_id=file_id)
        file_path = file.file_path
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
        
        # Путь для сохранения фотографии
        save_path = Path('static/media/users') / f'{file_id}.webp'
        save_path.parent.mkdir(parents=True, exist_ok=True)  # Создаем папку, если она не существует
        
        # Скачиваем и сохраняем фотографию
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    with open(save_path, 'wb') as f:
                        f.write(await response.read())


    user_reg = await add_user_data(user_id=message.from_user.id, photo=f'{file_id}.webp', username=message.from_user.username, first_name=message.from_user.first_name )

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
                            'Нажмите «Начать», чтобы открыть приложение!' ,reply_markup=kb.start_inline())
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
                            'Нажмите «Начать», чтобы открыть приложение!' ,reply_markup=kb.start_inline())


@user_private.callback_query(F.data.startswith("pay_"))
async def order_delivered_point(callback: CallbackQuery):
    data_id = callback.data.split("_")[1]
    n = await get_web_data_all(data_id=data_id)
    summa = n[0]['order_data']['Order']['info']['summa']
    tg_id = n[0]['order_data']['Order']['user']['tg_id']
    summa = float(summa) 
    tg_id = int(tg_id)
    confirmation_url,pay_id = create(summa, tg_id)


    await callback.message.edit_text(f'Оплатите заказ по ссылке ниже',reply_markup=kb.get_pay(confirmation_url, summa, pay_id, data_id))



@user_private.callback_query(F.data.startswith('check_'))
async def check_it(callback: CallbackQuery):
    tg_id = callback.from_user.id
    result = check(callback.data.split('_')[-1])
    order_id = callback.data.split('_')[-2]

    await callback.answer()

    if result:
        await callback.message.answer('Ошибка')
    else:
        # Отправка уведомления в чат о новой брони
        order_data = await get_web_data_all(order_id)
        if order_data:
            order_info = order_data[0]['order_data']
            username = callback.from_user.username
            phone_number = order_info['Order']['user']['phone']
            summa = order_info['Order']['info']['summa']
            discount = order_info['Order']['info']['discount']

            hall = list(order_info["Order"]["info"]["halls"].values())[0]
            hall_name = hall["name"]
            hall_datetime = hall["datetime"]
            hall_hours = hall["hours"]

            food_items = order_info["Order"]["info"]["food"].values()
            service_items = order_info["Order"]["info"]["services"].values()
            goods_items = order_info["Order"]["info"]["goods"].values()

            additional_items = []
            for food in food_items:
                additional_items.append(f'{food["name"]} ({food["weight"]} г.) — {food["price"]}₽ x {food["quantity"]}')
            for service in service_items:
                additional_items.append(f'{service["name"]} ({service["time"]} мин.) — {service["price"]}₽')
            for goods in goods_items:
                additional_items.append(f'{goods["name"]} ({goods["weight"]} мл.) — {goods["price"]}₽ x {goods["quantity"]}')

            additional_items_str = "\n".join(f"{i+1}. {item}" for i, item in enumerate(additional_items))

            notify_text = (
                f'🆕 Новая бронь от @{username}\n\n'
                f'Выбранный зал: {hall_name}\n'
                f'Дата: {hall_datetime}\n'
                f'Количество часов: {hall_hours}\n'
                f'Телефон: {phone_number}\n\n'
                f'Дополнительно:\n'
                f'{additional_items_str}\n\n'
                f'💳 Итоговая стоимость: {summa} ₽ (скидка {discount}%)'
            )

            await order_notify(-4500825826, notify_text)

        await callback.message.edit_text(
            '✅ Спасибо за покупку! Я буду \n'
            'присылать тебе уведомления \n'
            'об изменениях статуса заказа'
        )