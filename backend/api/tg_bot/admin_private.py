from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,WebAppInfo
from decimal import Decimal  # Добавьте этот импорт
import aiofiles
import os

from api.models import User, Booked, Halls, Foods
from api.tg_bot.database import *
from api.tg_bot.classes_functions import Admin
import api.tg_bot.reply as kb
from api.tg_bot.database import check_admin
from PIL import Image


admin_private = Router()




@admin_private.message(Command('admin'))
async def admin_panel(message: Message):
    ch = await check_admin(message.from_user.id)
    print(message)
    if ch:
        await message.answer('🔒 Админ-панель', reply_markup=kb.admin_panel())
    else:
        await message.answer('У вас нет доступа')

@admin_private.callback_query(F.data == 'statistics')
async def statistics(callback: CallbackQuery):
    await callback.answer()
    
    q = await get_users() 
    q2 = await get_users_status() 
    q3 = await get_users_status2() 
    
    total_orders = await get_total_bookings_count()
    today_orders = await get_today_bookings_count()
    week_orders = await get_week_bookings_count()
    month_orders = await get_month_bookings_count()
    
    await callback.message.answer('📊 <b>Статистика</b> \n'
                                  f'Всего пользователей: <b>{q}</b> \n'
                                  f'Активных пользователей: <b>{q2}</b> \n'
                                  f'Неактивных пользователей: <b>{q3}</b> \n'
                                  '\n'
                                  '📦 <b>Заказы</b> \n'
                                  f'Всего заказов: <b>{total_orders}</b>\n'
                                  f'Заказов сегодня: <b>{today_orders}</b>\n'
                                  f'Заказов за неделю: <b>{week_orders}</b>\n'
                                  f'Заказов за месяц: <b>{month_orders}</b>')





@admin_private.callback_query(F.data == 'mailing')
async def post_mailing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.mailing_state)

    await callback.message.answer('Выберите тип рассылки',reply_markup=kb.post_type())

@admin_private.message(Admin.mailing_state)
async def proccess_text(message: Message, state: FSMContext):
    if message.text == "Только текст":
        await state.set_state(Admin.mailing_text_only)

    elif message.text == "С фото":
        await state.set_state(Admin.mailing_text)
    await message.answer('Отправьте пост для рассылки',reply_markup=ReplyKeyboardRemove())

@admin_private.message(Admin.mailing_text_only)
async def proccess_text(message: Message, state: FSMContext):
    await state.update_data(mailing_text=message.text)
    await state.set_state(Admin.ask)
    await message.answer('Добавить кнопку \"<b>Забронировать</b>\"?')

@admin_private.message(Admin.mailing_text, F.photo)
async def proccess_text(message: Message, state: FSMContext):
    await state.update_data(mailing_text=message.caption)
    await state.update_data(mailing_photo=message.photo[-1].file_id)
    await state.set_state(Admin.ask)
    await message.answer('Добавить кнопку \"<b>Забронировать</b>\"?')


@admin_private.message(Admin.ask)
async def procces_ask(message: Message, state: FSMContext):
    await state.update_data(ask=message.text)
    data = await state.get_data()
    if 'mailing_photo' in data:
        photo = data['mailing_photo']
        caption = data['mailing_text']
        text = data['ask']

        if not text:
            text = ""

        if message.text == 'Да' or  message.text == 'да':
            await state.set_state(Admin.confirm_yes)
            await message.answer_photo(photo=photo, caption=f'{caption} \n'
                                    '\n'
                                    'Все верно?',
                                    reply_markup=kb.choice_button_yes())

        elif message.text == 'Нет' or  message.text == 'нет':
            await state.set_state(Admin.confirm_no)
            
            await message.answer_photo(photo=photo, caption=f'{caption} \n'
                                    '\n'
                                    'Все верно?',
                                    reply_markup=kb.choice_button_no())
    else:
        caption = data['mailing_text']
        text = data['ask']


        if message.text == 'Да' or  message.text == 'да':
            await state.set_state(Admin.confirm_yes)
            await message.answer(text=f'{caption} \n'
                                    '\n'
                                    'Все верно?',
                                    reply_markup=kb.choice_button_yes())

        elif message.text == 'Нет' or  message.text == 'нет':
            await state.set_state(Admin.confirm_no)
            await message.answer(text=f'{caption} \n'
                                    '\n'
                                    'Все верно?',
                                    reply_markup=kb.choice_button_yes())


@admin_private.message(Admin.confirm_yes)
async def procces_post_yes(message: Message, state: FSMContext):
    await state.update_data(confirm_yes=message.text)
    data = await state.get_data()
    text = data['confirm_yes']

    if text == 'Да, выполнить':
        # Здесь нужно сделать функцию рассылки с кнопкой
        z = await state.get_data()

        u = await get_users_post()
        if 'mailing_photo' in data:
            c = 0
            caption = data['mailing_text']
            photo = data['mailing_photo']
            for user in u:
                

                await message.bot.send_photo(user['tg_id'], photo=data['mailing_photo'], caption=caption,reply_markup=kb.get_order_post())
                c+=1
            await message.answer('Рассылка завершена \n'
                                f'Отправлено: <b>{c} сообщений</b>',
                                reply_markup=ReplyKeyboardRemove())
            await message.answer('Вы вернулись в меню', reply_markup=kb.admin_panel())
            await state.clear()
        else:
            c = 0
            for user in u:
                

                await message.bot.send_message(user['tg_id'],f'{data["mailing_text"]}',reply_markup=kb.get_order_post())
                c+=1
            await message.answer('Рассылка завершена \n'
                                f'Отправлено: <b>{c} сообщений</b>',
                                reply_markup=ReplyKeyboardRemove())
            await message.answer('Вы вернулись в меню', reply_markup=kb.admin_panel())
            await state.clear()

    if text == 'Нет, вернуться':
        if 'mailing_photo' in data:
            await state.clear()
            await state.set_state(Admin.mailing_text)
            await message.answer('Отправьте пост для рассылки', reply_markup=ReplyKeyboardRemove())
        else:
            await state.clear()
            await state.set_state(Admin.mailing_text_only)
            await message.answer('Отправьте пост для рассылки', reply_markup=ReplyKeyboardRemove())

@admin_private.message(Admin.confirm_no)
async def procces_post_no(message: Message, state: FSMContext):
    await state.update_data(confirm_yes=message.text)
    data = await state.get_data()
    # caption = data['mailing_text']
    # photo = data['mailing_photo']
    text = data['confirm_yes']

    if text == 'Да, выполнить':
        # Здесь нужно сделать функцию рассылки с кнопкой
        z = await state.get_data()

        u = await get_users_post()

        
        if 'mailing_photo' in data:
            c = 0
            caption = data['mailing_text']
            photo = data['mailing_photo']
            for user in u:
                

                await message.bot.send_photo(user['tg_id'], photo=data['mailing_photo'], caption=caption)
                c+=1
            await message.answer('Рассылка завершена \n'
                                f'Отправлено: <b>{c} сообщений</b>',
                                reply_markup=ReplyKeyboardRemove())
            await message.answer('Вы вернулись в меню', reply_markup=kb.admin_panel())
            await state.clear()
        else:
            c = 0
            for user in u:
                

                await message.bot.send_message(user['tg_id'],f'{data["mailing_text"]}')
                c+=1
            await message.answer('Рассылка завершена \n'
                                f'Отправлено: <b>{c} сообщений</b>',
                                reply_markup=ReplyKeyboardRemove())
            await message.answer('Вы вернулись в меню', reply_markup=kb.admin_panel())
            await state.clear()
    if text == 'Нет, вернуться':
        if 'mailing_photo' in data:
            await state.clear()
            await state.set_state(Admin.mailing_text)
            await message.answer('Отправьте пост для рассылки', reply_markup=ReplyKeyboardRemove())
        else:
            await state.clear()
            await state.set_state(Admin.mailing_text_only)
            await message.answer('Отправьте пост для рассылки', reply_markup=ReplyKeyboardRemove())     

import os
import hashlib

async def file_hash(file_path):
    """Calculate the hash of the file to detect duplicates."""
    hash_md5 = hashlib.md5()
    async with aiofiles.open(file_path, 'rb') as f:
        while True:
            chunk = await f.read(4096)
            if not chunk:
                break
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@admin_private.callback_query(F.data == 'add_hall')
async def add_hall(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.p_name)
    await callback.message.answer('Введите название зала', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.p_name)
async def add_hall_name(message: Message, state: FSMContext):
    user_message = message.text
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(p_name=user_message)
        await state.update_data(p_photos=[])  # Инициализируем список для фото
        await state.set_state(Admin.p_photo1)
        await message.answer('Отправьте фото 1.', reply_markup=kb.offer_cancel())

# Обработка нажатия кнопки "Дальше"
@admin_private.callback_query(F.data == 'next')
async def next_step(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    current_state = await state.get_state()
    if current_state.startswith("p_photo"):
        next_state = Admin.p_desc
        await state.set_state(next_state)
        await callback.message.answer('Введите описание зала.', reply_markup=kb.offer_cancel())



# Обработка фото 1
@admin_private.message(Admin.p_photo1, F.photo)
async def process_photo1(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo2, 'Отправьте фото 2.')

@admin_private.message(Admin.p_photo2, F.photo)
async def process_photo2(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo3, 'Отправьте фото 3.')

@admin_private.message(Admin.p_photo3, F.photo)
async def process_photo3(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo4, 'Отправьте фото 4.')

@admin_private.message(Admin.p_photo4, F.photo)
async def process_photo4(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo5, 'Отправьте фото 5.')

@admin_private.message(Admin.p_photo5, F.photo)
async def process_photo5(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo6, 'Отправьте фото 6.')

@admin_private.message(Admin.p_photo6, F.photo)
async def process_photo6(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo7, 'Отправьте фото 7.')

@admin_private.message(Admin.p_photo7, F.photo)
async def process_photo7(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo8, 'Отправьте фото 8.')

@admin_private.message(Admin.p_photo8, F.photo)
async def process_photo8(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo9, 'Отправьте фото 9.')

@admin_private.message(Admin.p_photo9, F.photo)
async def process_photo9(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_photo10, 'Отправьте фото 10.')

from aiogram.fsm.state import State, StatesGroup


# Обработка фото 10
@admin_private.message(Admin.p_photo10, F.photo)
async def process_photo10(message: Message, state: FSMContext):
    await save_photo(message, state, Admin.p_desc, 'Все фото сохранены. Введите описание зала.')

# Функция для сохранения фото и перехода к следующему состоянию
async def save_photo(message: Message, state: FSMContext, next_state: State, next_prompt: str):
    if next_prompt == '↩️ Вернуться':
        state.clear()
        await state.set_state(Admin.p_name)
        await message.answer('Введите название зала', reply_markup=kb.offer_cancel())
    else:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        file_name = f"static/media/halls/{file_id}.webp"

        # Скачиваем фото
        file = await message.bot.download_file(file_path)

        # Конвертируем фото в формат webp
        with Image.open(file) as img:
            img.save(file_name, format='webp')
            
        data = await state.get_data()
        photos = data.get('p_photos', [])
        photos.append(file_name)
        await state.update_data(p_photos=photos)

        await state.set_state(next_state)
        await message.answer(next_prompt, reply_markup=kb.photo_menu)


@admin_private.message(Admin.p_photo1, F.text)
@admin_private.message(Admin.p_photo2, F.text)
@admin_private.message(Admin.p_photo3, F.text)
@admin_private.message(Admin.p_photo4, F.text)
@admin_private.message(Admin.p_photo5, F.text)
@admin_private.message(Admin.p_photo6, F.text)
@admin_private.message(Admin.p_photo7, F.text)
@admin_private.message(Admin.p_photo8, F.text)
@admin_private.message(Admin.p_photo9, F.text)
@admin_private.message(Admin.p_photo10, F.text)
async def handle_photo_navigation(message: Message, state: FSMContext):
    
    await state.set_state(Admin.p_desc)
    await message.answer('Введите описание зала.', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.p_desc)
async def add_hall_description(message: Message, state: FSMContext):
    user_message = message.text
    if user_message == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(p_desc=user_message)
        await state.set_state(Admin.p_capacity)
        await message.answer('Введите вместимость зала (число)', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.p_capacity)
async def add_hall_capacity(message: Message, state: FSMContext):
    user_message = message.text
    if user_message == 'Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(p_capacity=user_message)
        await state.set_state(Admin.p_price)
        await message.answer('Введите цену за час (число)', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.p_price)
async def add_hall_price(message: Message, state: FSMContext):
    user_message = message.text
    try:
        cost = Decimal(user_message)
        data = await state.get_data()
        hall_name = data['p_name']
        hall_description = data['p_desc']
        hall_capacity = data['p_capacity']
        hall_photos = ",".join(data['p_photos'])  # Фото сохранены в строке, разделенной запятыми
        # Создание объекта зала
        hall = await sync_to_async(Halls.objects.create)(
            name=hall_name,
            desc=hall_description,
            max_people=hall_capacity,
            price=cost,
            photo=hall_photos  # Сохраняем фото в поле, разделенные запятыми
        )

        await message.answer(f'✅ Зал "{hall_name}" успешно добавлен.')
        await admin_panel(message)
        await state.clear()
    except Exception as e:
        await message.answer(f'Ошибка: {str(e)}. Попробуйте еще раз.')
        await state.set_state(Admin.p_price)


async def admin_panel(message: Message):
    await message.answer('Админ панель', reply_markup=kb.admin_panel())


@admin_private.callback_query(F.data == 'add_come_out')
async def come_out_menu(callback: CallbackQuery):
    await callback.message.edit_text('🔒 Админ-панель', reply_markup=kb.admin_panel())

@admin_private.callback_query(F.data == 'delete_smth')
async def delete_smth(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Выбирете категорию', reply_markup=kb.delete_categories())

@admin_private.callback_query(F.data == 'add_service')
async def add_service(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Выбирете категорию', reply_markup=kb.add_categories())


# Функция для сохранения фото и перехода к следующему состоянию
async def save_photo2(message: Message, state: FSMContext, next_state: State, next_prompt: str):
    if next_prompt == '↩️ Вернуться':
        state.clear()
        await state.set_state(Admin.p_name)
        await message.answer('Введите название зала', reply_markup=kb.offer_cancel())
    else:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        file_name = f"static/media/foods/{file_id}.webp"

        # Скачиваем фото
        file = await message.bot.download_file(file_path)

        # Конвертируем фото в формат webp
        with Image.open(file) as img:
            img.save(file_name, format='webp')
            

        await state.update_data(s_photo=file_name)

        await state.set_state(next_state)
        await message.answer(next_prompt, reply_markup=kb.offer_cancel())


@admin_private.callback_query(F.data == 'add_foods')
async def add_foods(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.s_type1)

    await callback.message.answer('Введите название позиции', reply_markup=kb.offer_cancel())


@admin_private.message(Admin.s_type1)
async def add_type1(message: Message, state: FSMContext):
    user_message = message.text
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(type_for=1)
        await state.update_data(s_name=message.text)
        await state.set_state(Admin.s_photo)
        await message.answer('Отправьте фото позиции', reply_markup=kb.offer_cancel())



@admin_private.message(Admin.s_photo, F.photo)
async def process_s_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    type_for = data['type_for']
    if type_for == 1:
        await save_photo2(message, state, Admin.s_desc, 'Введите описание позиции')
    elif type_for == 2:
        await save_photo3(message, state, Admin.s_desc, 'Введите описание позиции')
    elif type_for == 3:
        await save_photo4(message, state, Admin.s_desc, 'Введите описание позиции')

@admin_private.message(Admin.s_photo, F.text)
async def process_s_photo_text(message: Message, state: FSMContext):
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.set_state(Admin.s_photo)
        await message.answer('Отправьте фото', reply_markup=kb.offer_cancel())


@admin_private.message(Admin.s_desc)
async def process_s_desc(message: Message, state: FSMContext):
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        data = await state.get_data()
        type_for = data['type_for']
        if type_for == 2:
            await state.set_state(Admin.s_price)
            await message.answer('Введите стоимость (только число)', reply_markup=kb.offer_cancel())
        else:
            await state.update_data(s_desc=message.text)
            await state.set_state(Admin.s_weight)
            await message.answer('Введите вес товара или другой параметр\n'
                                '\n'
                                'Например, 100 мл. или 10 гр.', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.s_weight)
async def process_s_weight(message: Message, state: FSMContext):
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        data = await state.get_data()
        type_for = data['type_for']
        if type_for == 2:
            await state.set_state(Admin.s_price)
            await message.answer('Введите стоимость (только число)', reply_markup=kb.offer_cancel())
        elif type_for == 1:
            await state.update_data(s_weight=message.text)
            await state.set_state(Admin.s_kitchen)
            await message.answer('Введите тип кухни', reply_markup=kb.offer_cancel())
        else:
            await state.set_state(Admin.s_price)
            await message.answer('Введите цену позиции', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.s_kitchen)
async def process_s_kitchen(message: Message, state: FSMContext):
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(s_kitchen=message.text)
        await state.set_state(Admin.s_compound)
        await message.answer('Введите состав позиции через запятую', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.s_compound)
async def process_s_compound(message: Message, state: FSMContext):
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(s_compound=message.text)
        await state.set_state(Admin.s_price)
        await message.answer('Введите цену позиции', reply_markup=kb.offer_cancel())

@admin_private.message(Admin.s_price)
async def process_s_price(message: Message, state: FSMContext):
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(s_price=message.text)
        # Получаем данные из состояния
        data = await state.get_data()
        photo = data.get('s_photo')
        weight = data.get('s_weight')
        name = data.get('s_name')
        kitchen = data.get('s_kitchen')
        compounds = data.get('s_compound')
        status = Foods.StatusEnum.EXISTS
        price = data.get('s_price')
        # Сохраняем объект в базу данных асинхронно
        await save_food(photo, weight, name, kitchen, compounds, status, price)
        await message.answer('✅ Позиция успешно добавлена', reply_markup=kb.admin_panel())
        await state.clear()




# Функция для сохранения фото и перехода к следующему состоянию
async def save_photo3(message: Message, state: FSMContext, next_state: State, next_prompt: str):
    if next_prompt == '↩️ Вернуться':
        state.clear()
        await state.set_state(Admin.p_name)
        await message.answer('Введите название зала', reply_markup=kb.offer_cancel())
    else:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        file_name = f"static/media/services/{file_id}.webp"

        # Скачиваем фото
        file = await message.bot.download_file(file_path)

        # Конвертируем фото в формат webp
        with Image.open(file) as img:
            img.save(file_name, format='webp')
            

        await state.update_data(s_photo=file_name)

        await state.set_state(next_state)
        await message.answer(next_prompt, reply_markup=kb.offer_cancel())


@admin_private.callback_query(F.data == 'add_services')
async def add_services(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.s_type2)

    await callback.message.answer('Введите название позиции', reply_markup=kb.offer_cancel())


@admin_private.message(Admin.s_type2)
async def add_type2(message: Message, state: FSMContext):
    user_message = message.text
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(type_for=2)
        await state.update_data(s_name=message.text)
        await state.set_state(Admin.s_photo)
        await message.answer('Отправьте фото позиции', reply_markup=kb.offer_cancel())




@admin_private.callback_query(F.data == 'add_goods')
async def add_goods(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.s_type3)

    await callback.message.answer('Введите название позиции', reply_markup=kb.offer_cancel())


@admin_private.message(Admin.s_type3)
async def add_type3(message: Message, state: FSMContext):
    user_message = message.text
    if message.text == '↩️ Вернуться':
        await message.answer('Вы отменили действие', reply_markup=ReplyKeyboardRemove())
        await message.answer('Админ панель', reply_markup=kb.admin_panel())
        await state.clear()
    else:
        await state.update_data(type_for=3)
        await state.update_data(s_name=message.text)
        await state.set_state(Admin.s_photo)
        await message.answer('Отправьте фото позиции', reply_markup=kb.offer_cancel())



async def save_photo4(message: Message, state: FSMContext, next_state: State, next_prompt: str):
    if next_prompt == '↩️ Вернуться':
        state.clear()
        await state.set_state(Admin.p_name)
        await message.answer('Введите название зала', reply_markup=kb.offer_cancel())
    else:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        file_name = f"static/media/goods/{file_id}.webp"

        # Скачиваем фото
        file = await message.bot.download_file(file_path)

        # Конвертируем фото в формат webp
        with Image.open(file) as img:
            img.save(file_name, format='webp')
            

        await state.update_data(s_photo=file_name)

        await state.set_state(next_state)
        await message.answer(next_prompt, reply_markup=kb.offer_cancel())





@admin_private.callback_query(F.data == 'add_foods')
async def add_foods(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.s_type1)

    await callback.message.answer('Введите название позиции', reply_markup=kb.offer_cancel())

