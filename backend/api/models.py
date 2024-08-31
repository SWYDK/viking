from django.db import models
from django.utils.translation import gettext_lazy as _




class User(models.Model):
    class ThemeEnum(models.TextChoices):
        DARK = 'DK', _('Dark')
        LIGHT = 'LI', _('Light')
        
    tg_id = models.BigIntegerField('Telegram ID')
    photo = models.ImageField('Аватарка пользователя',null=True, upload_to='static/media/users/')
    tg_username = models.CharField('Имя пользователя',null=True, max_length=250, blank=True)
    name = models.CharField('Имя', max_length=300,null=True, blank=True)
    user_theme = models.CharField('Цвет приложения', choices=ThemeEnum.choices, default=ThemeEnum.LIGHT, max_length=250)
    phone_number = models.CharField('Номер телефона', max_length=200, null=True)
    reg_date = models.DateField('Время регистрации', auto_now=True)
    isActive = models.BooleanField('Активен', default=False)


    list_per_page = 500

    def __str__(self):
        return str(self.tg_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Admins(models.Model):
    tg_id = models.BigIntegerField('Админы')
    list_per_page = 500

    def __str__(self):
        return str(self.tg_id)

    class Meta:
        verbose_name = 'Админ'
        verbose_name_plural = 'Админы'


class Halls(models.Model):
    class StatusEnum(models.TextChoices):
        FREE = 'FR', _('Free')
        BUSY = 'BS', _('Busy')
        
    photo = models.ImageField('Аватарка пользователя', upload_to='static/media/halls/')
    max_people = models.IntegerField('Макс. человек', blank=True )
    name = models.CharField('Имя зала', max_length=300, blank=True)
    desc = models.TextField('Описание', blank=True)
    status = models.CharField('Статус', choices=StatusEnum.choices, default=StatusEnum.FREE, max_length=250)
    price = models.IntegerField('Цена', blank=True)

    list_per_page = 500

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'


class Foods(models.Model):
    class StatusEnum(models.TextChoices):
        EXISTS = 'EX', _('Exists')
        EMPTY = 'EM', _('Empty')
        PRESENT = 'PR', _('Present')

        
    photo = models.ImageField('Фото', upload_to='static/media/foods/')
    weight = models.IntegerField('Масса еды', blank=True )
    name = models.CharField('Имя', max_length=300, blank=True)
    kitchen = models.CharField('Тип кухни', max_length=300, null=True, blank=True)
    compounds = models.CharField('Состав', max_length=300, null=True, blank=True)
    status = models.CharField('Статус', choices=StatusEnum.choices, default=StatusEnum.EXISTS, max_length=250)
    price = models.IntegerField('Цена в руб', blank=True)

    list_per_page = 500

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Еда/Закуска'
        verbose_name_plural = 'Еды/Закуски'

class Services(models.Model):
    
        
    photo = models.ImageField('Фото', upload_to='static/media/services/')
    for_time = models.IntegerField('Время услуги в минутах', blank=True )
    name = models.CharField('Имя', max_length=300, blank=True)
    price = models.IntegerField('Цена в руб', blank=True)

    list_per_page = 500

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Goods(models.Model):
    class StatusEnum(models.TextChoices):
        EXISTS = 'EX', _('Exists')
        EMPTY = 'EM', _('Empty')
        
    photo = models.ImageField('Фото', upload_to='static/media/goods/')
    weight = models.CharField('Объем/Масса',null=True, max_length=300, blank=True )
    name = models.CharField('Имя', max_length=300, blank=True)
    status = models.CharField('Статус', choices=StatusEnum.choices, default=StatusEnum.EXISTS, max_length=250)
    price = models.IntegerField('Цена в руб', blank=True)

    list_per_page = 500

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class CartFood(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f'{self.food.name} - {self.quantity} шт.'

class CartService(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f'{self.service.name} - {self.quantity} шт.'

class CartGoods(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f'{self.goods.name} - {self.quantity} шт.'

class Cart(models.Model):
    hall = models.ForeignKey(Halls, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_time = models.DateTimeField('Время бронирования', null=False)
    booking_time = models.IntegerField('Количество забронированных часов')
    foods = models.ManyToManyField(Foods, through=CartFood, blank=True, related_name='cart_bookings')
    services = models.ManyToManyField(Services, through=CartService, blank=True, related_name='cart_bookings')
    goods = models.ManyToManyField(Goods, through=CartGoods, blank=True, related_name='cart_bookings')

    list_per_page = 500

    def __str__(self):
        return f'{self.user.name} на {self.book_time}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class Booked(models.Model):
    
    hall = models.ForeignKey(Halls, on_delete=models.CASCADE)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField('Время создания брони', auto_now=True ,null=True)
    book_time = models.DateTimeField('Время бронирования', null=False)
    booking_time = models.IntegerField('Количество забронированных часов')
    foods = models.ManyToManyField(Foods, blank=True, related_name='bookings')

    services = models.ManyToManyField(Services, blank=True, related_name='bookings')
    goods = models.ManyToManyField(Goods, blank=True, related_name='bookings')
    reminder_sent_hour = models.BooleanField(default=False)
    reminder_sent_day = models.BooleanField(default=False)
    reminder_sent_week = models.BooleanField(default=False)


    

    list_per_page = 500

    def __str__(self):
        return f'{self.user.name} на {self.book_time}'

    class Meta:
        verbose_name = 'Забронировано'
        verbose_name_plural = 'Забронированы'

class SMS(models.Model):
    
    phone_number = models.CharField("Номер телефона", max_length=250)
    need_code = models.IntegerField("Нужный код из смс", null=True)


    list_per_page = 500

    def __str__(self):
        return f'{self.user.name} на {self.book_time}'

    class Meta:
        verbose_name = 'Подтверждение'
        verbose_name_plural = 'Подтверждения'


class Notify(models.Model):
    
    tg_id = models.CharField("Telegram ID", max_length=250)
    msg = models.TextField("Сообщение", null=True)


    list_per_page = 500

    def __str__(self):
        return f'{self.tg_id} - {self.msg}'

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'

class Presents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.ForeignKey(Foods, on_delete=models.CASCADE)



    list_per_page = 500

    def __str__(self):
        return f'{self.tg_id} - {self.msg}'

    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'

class WebAppData(models.Model):
    
    order_data = models.JSONField()
    is_viewed = models.BooleanField(default=False)

    list_per_page = 500

    def __str__(self):
        return f'Данные WebApp'

    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Данные'