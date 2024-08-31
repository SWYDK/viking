from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,WebAppInfo
from api.tg_bot.database import *


def admin_panel() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Статистика', callback_data='statistics')
    keyboard.button(text='Рассылка', callback_data='mailing')
    keyboard.button(text='Добавить зал', callback_data='add_hall')
    keyboard.button(text='Добавить товар/услугу', callback_data='add_service')
    keyboard.button(text='Удалить зал или товар', callback_data='delete_smth')
    return keyboard.adjust(1).as_markup()

def get_pay(confirmation_url,amount,pay_id,order_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=f'💳 Банковская карта {amount} ₽', web_app=WebAppInfo(text='Начать',url=confirmation_url))
    keyboard.button(text='Проверить', callback_data=f'check_{order_id}_{pay_id}')

    return keyboard.adjust(1).as_markup()


def photo_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=f'Добавить фото', callback_data="add_more_photos")
    keyboard.button(text='Продолжить', callback_data=f'continue_add_hall')

    return keyboard.adjust(1).as_markup()

photo_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='↩️ Вернуться')
        ],
        [
            KeyboardButton(text='Продолжить')
        ]
        
    ],
    resize_keyboard=True
)

def start_inline() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=f'👉 Начать', web_app=WebAppInfo(text='Начать',url='https://pizzafresca.ru'))

    return keyboard.adjust(1).as_markup()

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👉 Начать',  web_app=WebAppInfo(text='Начать',url='https://pizzafresca.ru/reg'))
        ],
        
    ],
    resize_keyboard=True
)

start_menu_for_reg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👉 Начать',  web_app=WebAppInfo(text='Начать',url='https://pizzafresca.ru'))
        ],
        
    ],
    resize_keyboard=True
)





def check_order(data_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Оплатить', callback_data=f'pay_{data_id}')
    keyboard.button(text='Отмена', callback_data='cancel_payment')
    return keyboard.adjust(1).as_markup()


def add_categories() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Еда', callback_data='add_foods')
    keyboard.button(text='Услуги', callback_data='add_services')
    keyboard.button(text='Товары', callback_data='add_goods')
    keyboard.button(text=' ↩️ Выйти', callback_data='add_come_out')
    return keyboard.adjust(2).as_markup()


def delete_categories() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Еда', callback_data='delete_foods')
    keyboard.button(text='Услуги', callback_data='delete_services')
    keyboard.button(text='Товары', callback_data='delete_goods')
    keyboard.button(text='Залы', callback_data='delete_halls')
    keyboard.button(text='Выйти', callback_data='delete_come_out')
    return keyboard.adjust(2).as_markup()


def offer_cancel() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='↩️ Вернуться')
    return keyboard.as_markup(resize_keyboard=True)



def choice_button_yes() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Да, выполнить')
    keyboard.button(text='Нет, вернуться')
    return keyboard.as_markup(resize_keyboard=True)

def post_type() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Только текст')
    keyboard.button(text='С фото')
    return keyboard.as_markup(resize_keyboard=True)


def choice_button_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Да, выполнить')
    keyboard.button(text='Нет, вернуться')
    return keyboard.as_markup(resize_keyboard=True)


def get_order_post():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Забронировать', web_app=WebAppInfo(text='Забронировать', url='https://google.com') )
    return keyboard.adjust(1).as_markup()

