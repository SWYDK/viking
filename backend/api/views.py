
from .models import (User, Halls, Foods, Booked, Goods, 
Services, SMS, Cart, CartFood, CartService, CartGoods,WebAppData)
from .serializers import (
    UserSerializer, HallsSerializer, FoodsSerializer, BookedSerializer,
    ServicesSerializer, GoodsSerializer, CartSerializer,
    CartFoodSerializer, CartServiceSerializer, CartGoodsSerializer,SMSSerializer, WebAppDataSerializer
)
import requests
import random
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def get_datetime(self, request):
        # Получаем текущие дату и время
        current_datetime = timezone.now()
        return Response({'datetime': current_datetime})

    @action(detail=False, methods=['get'])
    def get_by_tg_id(self, request):
        tg_id = request.query_params.get('tg_id')
        if not tg_id:
            return Response({'error': 'tg_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(tg_id=tg_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)
        return Response(serializer.data)
        

class HallsViewSet(viewsets.ModelViewSet):
    queryset = Halls.objects.all()
    serializer_class = HallsSerializer

    @action(detail=False, methods=['get'])
    def get_by_name(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hall = Halls.objects.get(name=name)
        except Halls.DoesNotExist:
            return Response({'error': 'Hall not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(hall)
        return Response(serializer.data)
        
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

class WebAppDataViewSet(viewsets.ModelViewSet):
    queryset = WebAppData.objects.all()
    serializer_class = WebAppDataSerializer


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