from rest_framework import viewsets
from .models import User, Halls, Foods, Booked, Goods, Services, SMS, Cart, CartFood, CartService, CartGoods
from .serializers import (
    UserSerializer, HallsSerializer, FoodsSerializer, BookedSerializer,
    ServicesSerializer, GoodsSerializer, CartSerializer,
    CartFoodSerializer, CartServiceSerializer, CartGoodsSerializer,SMSSerializer
)
import requests
import random
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HallsViewSet(viewsets.ModelViewSet):
    queryset = Halls.objects.all()
    serializer_class = HallsSerializer


class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializer


class BookedViewSet(viewsets.ModelViewSet):
    queryset = Booked.objects.all()
    serializer_class = BookedSerializer


class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer


class SMSViewSet(viewsets.ModelViewSet):
    queryset = SMS.objects.all()
    serializer_class = SMSSerializer

    @action(detail=False, methods=['post'])
    def send_sms(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'status': '400', 'message': 'Номер телефона не указан'})

        # Генерация случайного 6-значного кода
        code = random.randint(100000, 999999)

        # Отправка SMS через API
        api_url = "https://smsc.ru/sys/send.php"
        params = {
            "login": "VIKING62",  # Вставьте ваш логин
            "psw": "E559cK62",  # Вставьте ваш пароль
            "phones": phone_number,
            "mes": f"Ваш код: {code}",
        }
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            # Сохранение номера телефона и кода в базе данных
            sms = SMS(phone_number=phone_number, need_code=code)
            sms.save()
            return Response({'status': '200', 'message': 'SMS успешно отправлено', 'data': {'phone_number': phone_number, 'code': code}})
        else:
            return Response({'status': '500', 'message': 'Ошибка при отправке SMS'})



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartFoodViewSet(viewsets.ModelViewSet):
    queryset = CartFood.objects.all()
    serializer_class = CartFoodSerializer

class CartServiceViewSet(viewsets.ModelViewSet):
    queryset = CartService.objects.all()
    serializer_class = CartServiceSerializer

class CartGoodsViewSet(viewsets.ModelViewSet):
    queryset = CartGoods.objects.all()
    serializer_class = CartGoodsSerializer