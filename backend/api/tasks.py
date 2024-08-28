import threading
import time
from django.utils import timezone
from .models import Booked, Notify
from datetime import timedelta
import requests
import pytz
from aiogram import Bot
from asgiref.sync import sync_to_async

def send_telegram_message(user, hall_name, book_time, reminder_type):
    token = '7420958680:AAEIWUXyQisXfiyeMR7jMT6XhYkyBTw4XYI'  # Замените на токен вашего бота
    chat_id = user.tg_id  # Telegram ID пользователя

    moscow_tz = pytz.timezone('Europe/Moscow')
    book_time_msk = book_time.astimezone(moscow_tz)
    if reminder_type == 'hour':
        text = f"🔔 Напоминаем, что через 1 час у вас назначена бронь зала «{hall_name}» ({book_time_msk.strftime('%d.%m.%y в %H:%M')})"
    elif reminder_type == 'day':
        text = f"🔔 Напоминаем, что через 1 день у вас назначена бронь зала «{hall_name}» ({book_time_msk.strftime('%d.%m.%y в %H:%M')})"
    elif reminder_type == 'week':
        text = f"🔔 Напоминаем, что через 1 неделю у вас назначена бронь зала «{hall_name}» ({book_time_msk.strftime('%d.%m.%y в %H:%M')})"
    else:
        return  # Если reminder_type не распознан, не отправляем сообщение

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    Notify.objects.create(
        tg_id=user.tg_id,
        msg=text
    )


def check_reminders():
    now = timezone.localtime(timezone.now())  # Текущее время с учетом часового пояса
    bookings = Booked.objects.filter(book_time__gte=now)

    for booking in bookings:
        # Время начала брони
        book_time = booking.book_time

        # Разница между текущим временем и временем бронирования
        time_diff = book_time - now
        time_until_booking = booking.book_time - now
        # Если осталось ровно 1 час
        if time_until_booking <= timedelta(hours=1) and time_until_booking > timedelta(minutes=59):
            print(booking.reminder_sent_hour)
            if not booking.reminder_sent_hour:
                send_telegram_message(booking.user, booking.hall.name, book_time, 'hour')
                booking.reminder_sent_hour = True  # Отмечаем, что часовое напоминание было отправлено
                booking.save()

        # Если осталось ровно 1 день
        elif time_until_booking <= timedelta(days=1) and time_until_booking > timedelta(hours=23):
            if not booking.reminder_sent_day:
                send_telegram_message(booking.user, booking.hall.name, book_time, 'day')
                booking.reminder_sent_day = True  # Отмечаем, что дневное напоминание было отправлено
                booking.save()

        # Если осталось ровно 1 неделя
        elif time_until_booking <= timedelta(weeks=1) and time_until_booking > timedelta(days=6):
            if not booking.reminder_sent_week:
                send_telegram_message(booking.user, booking.hall.name, book_time, 'week')
                booking.reminder_sent_week = True  # Отмечаем, что недельное напоминание было отправлено
                booking.save()


def run_reminder_scheduler():
    while True:
        now = timezone.localtime(timezone.now())  # Время с учетом часового пояса
        if now.minute == 0:
            check_reminders()
            print("Checking...")
            time.sleep(61)  
        if now.minute == 30:
            check_reminders()
            print("Checking...")
            time.sleep(61)  


def start_scheduler():
    thread = threading.Thread(target=run_reminder_scheduler, daemon=True)
    thread.start()
