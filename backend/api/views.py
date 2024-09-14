
from .models import (User, Halls, Foods, Booked, Goods,  History, Support, FiltersData, Presents,
Services, SMS, WebAppData)
from .serializers import (
    UserSerializer, HallsSerializer, FoodsSerializer, BookedSerializer,
    ServicesSerializer, GoodsSerializer,SMSSerializer, WebAppDataSerializer, HistorySerializer, SupportSerializer, FiltersDataSerializer, PresentsSerializer
)
import requests
import random
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta

class PresentsViewSet(viewsets.ModelViewSet):
    queryset = Presents.objects.all()
    serializer_class = PresentsSerializer


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    @action(detail=False, methods=['get'])
    def history_by_id(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        
        # Фильтруем записи по user_id
        history = History.objects.filter(user_id=user_id)
        serializer = HistorySerializer(history, many=True)
        return Response(serializer.data)
class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    
class FiltersDataViewSet(viewsets.ModelViewSet):
    queryset = FiltersData.objects.all()
    serializer_class = FiltersDataSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def calculate_order(self, request):
        # Получаем данные из тела запроса
        order_info = request.data.get('info', {})

        total_sum = 0
        discount = 0
        result_data = {"halls": {}, "food": {}, "goods": {}, "services": {}}

        # Расчет стоимости залов
        if 'halls' in order_info:
            for hall_id, hall_info in order_info['halls'].items():
                hall_obj = Halls.objects.get(id=hall_id)
                hall_hours = int(hall_info['hours'])
                hall_price_per_hour = hall_obj.price
                hall_total = hall_hours * hall_price_per_hour

                # Определение скидки для залов
                if hall_hours >= 6:
                    discount = 15
                elif hall_hours == 5:
                    discount = 12
                elif hall_hours == 4:
                    discount = 9
                elif hall_hours == 3:
                    discount = 7
                else:
                    discount = 0

                total_sum += hall_total

                # Собираем информацию о зале в один объект
                result_data["halls"][hall_id] = {
                    "name": hall_obj.name,
                    "desc": hall_obj.desc,
                    "max_people": hall_obj.max_people,
                    "status": hall_obj.status,
                    "photo": hall_obj.photo,
                    "hours": hall_hours,
                    "price_per_hour": hall_price_per_hour,
                    "total_price": hall_total
                }

        # Расчет стоимости еды
        if 'food' in order_info:
            for food_id, food_info in order_info['food'].items():
                food_obj = Foods.objects.get(id=food_id)
                food_quantity = int(food_info['quantity'])
                food_price = food_obj.price
                total_food_price = food_price * food_quantity
                total_sum += total_food_price

                # Собираем информацию о еде в один объект
                result_data["food"][food_id] = {
                    "name": food_obj.name,
                    "weight": food_obj.weight,
                    "kitchen": food_obj.kitchen,
                    "compounds": food_obj.compounds,
                    "status": food_obj.status,
                    "photo": food_obj.photo.url if food_obj.photo else None,
                    "quantity": food_quantity,
                    "price_per_unit": food_price,
                    "total_price": total_food_price
                }

        # Расчет стоимости услуг
        if 'services' in order_info:
            for service_id, service_info in order_info['services'].items():
                service_obj = Services.objects.get(id=service_id)
                total_price = service_obj.price 

                result_data["services"][service_id] = {
                    "name": service_obj.name, 
                    "photo": service_obj.photo.url if service_obj.photo else None,
                    "total_price": total_price  #
                }

        # Расчет стоимости товаров
        if 'goods' in order_info:
            for goods_id, goods_info in order_info['goods'].items():
                goods_obj = Goods.objects.get(id=goods_id)
                goods_quantity = int(goods_info['quantity'])
                goods_price = goods_obj.price
                total_goods_price = goods_price * goods_quantity
                total_sum += total_goods_price

                # Собираем информацию о товаре в один объект
                result_data["goods"][goods_id] = {
                    "name": goods_obj.name,
                    "weight": goods_obj.weight,
                    "status": goods_obj.status,
                    "photo": goods_obj.photo.url if goods_obj.photo else None,
                    "quantity": goods_quantity,
                    "price_per_unit": goods_price,
                    "total_price": total_goods_price
                }

        # Применение скидки
        total_sum_with_discount = total_sum - (total_sum * (discount / 100))

        result_data['total_sum'] =  round(total_sum, 2)
        result_data['total_sum_with_discount'] =  round(total_sum_with_discount, 2)
        result_data['discount'] = discount

        return Response(result_data)

    # POST - добавление данных в корзину
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        user = self.get_object()
        hall_id = request.data.get('hall_id')
        book_time = request.data.get('book_time')
        booking_time = request.data.get('booking_time')
        data = request.data.get('data')
        
        if hall_id:
            user.hall = get_object_or_404(Halls, id=hall_id)
        if book_time:
            user.book_time = book_time
        if booking_time:
            user.booking_time = booking_time
        if data:
            user.data = data
        
        user.save()
        hall_data = HallsSerializer(user.hall).data if user.hall else None
        return Response({'status': 'Items added to cart', 'hall': hall_data}, status=status.HTTP_201_CREATED)

    # PUT - обновление данных корзины
    @action(detail=True, methods=['put'])
    def update_cart(self, request, pk=None):
        user = self.get_object()
        hall_id = request.data.get('hall_id')
        book_time = request.data.get('book_time')
        booking_time = request.data.get('booking_time')
        data = request.data.get('data')

        if hall_id:
            user.hall = get_object_or_404(Halls, id=hall_id)
        if book_time:
            user.book_time = book_time
        if booking_time:
            user.booking_time = booking_time
        if data:
            user.data = data

        user.save()
        hall_data = HallsSerializer(user.hall).data if user.hall else None
        return Response({'status': 'Cart updated successfully', 'hall': hall_data}, status=status.HTTP_200_OK)

    # DELETE - очистка данных корзины
    @action(detail=True, methods=['delete'])
    def clear_cart(self, request, pk=None):
        user = self.get_object()
        user.hall = None
        user.book_time = None
        user.booking_time = None
        user.data = None
        user.save()
        return Response({'status': 'Cart cleared successfully'}, status=status.HTTP_204_NO_CONTENT)



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

    @action(detail=False, methods=['get'], url_path='filtered')
    def get_filtered_halls(self, request):
        max_people = request.query_params.get('max_people')
        max_price = request.query_params.get('max_price')
        date_str = request.query_params.get('date')  # Ожидаемый формат 'YYYY-MM-DD'
        time_str = request.query_params.get('time')  # Ожидаемый формат 'HH:MM'
        booking_duration = int(request.query_params.get('hours', 1))  # Количество часов бронирования, по умолчанию 1
        sort_type = request.query_params.get('type', '1')  # Тип сортировки (по умолчанию 1)

        # Фильтрация по максимальному количеству людей и цене
        queryset = self.queryset
        if max_people:
            queryset = queryset.filter(max_people__lte=max_people)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Парсинг даты и времени из запроса
        if date_str and time_str:
            datetime_str = f"{date_str} {time_str}"
            requested_datetime = parse_datetime(datetime_str)
            
            if requested_datetime:
                # Преобразование naive datetime в aware datetime (если необходимо)
                if timezone.is_naive(requested_datetime):
                    requested_datetime = timezone.make_aware(requested_datetime, timezone.get_current_timezone())
                
                # Время начала и конца бронирования с учетом времени уборки
                start_time = requested_datetime - timedelta(hours=2)  # 2 часа до начала бронирования
                end_time = requested_datetime + timedelta(hours=booking_duration + 2)  # Длительность бронирования + 2 часа на уборку

                # Получаем все залов, которые забронированы на любое время в этом интервале
                booked_halls = Booked.objects.filter(
                    # Проверяем, что время бронирования перекрывается с нашим интервалом
                    book_time__lt=end_time,
                    book_time__gte=start_time - timedelta(hours=2),
                    book_time__lte=end_time + timedelta(hours=2)  # Учитываем окончание бронирования
                )

                # Идентификаторы залов, которые будут забронированы
                occupied_halls = set()
                for booking in booked_halls:
                    booking_start = booking.book_time
                    booking_end = booking.book_time + timedelta(hours=booking.booking_time)
                    # Добавляем зал в список забронированных, если он перекрывается с нашим интервалом
                    if not (booking_end <= start_time or booking_start >= end_time):
                        occupied_halls.add(booking.hall_id)

                # Исключаем забронированные залы
                queryset = queryset.exclude(id__in=occupied_halls)

        # Определение порядка сортировки
        if sort_type == '1':
            # Сортировка по цене от меньшей к большей, затем по вместимости от большей к меньшей
            queryset = queryset.order_by('price', '-max_people')
        elif sort_type == '2':
            # Сортировка по вместимости от большей к меньшей, затем по цене от меньшей к большей
            queryset = queryset.order_by('-max_people', 'price')
        else:
            
            queryset = queryset.order_by('price', 'max_people')

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], url_path='check_hall')
    def check_hall(self, request):
        name = request.query_params.get('hall_id')
        date_str = request.query_params.get('date')  # Ожидаемый формат 'YYYY-MM-DD'
        time_str = request.query_params.get('time')  # Ожидаемый формат 'HH:MM'
        booking_duration = int(request.query_params.get('hours', 1))  # Длительность бронирования, по умолчанию 1

        if not name or not date_str or not time_str:
            return Response({'error': 'Required parameters: name, date, time, and hours'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка наличия зала
        try:
            hall = Halls.objects.get(id=name)
        except Halls.DoesNotExist:
            return Response({'error': 'Hall not found'}, status=status.HTTP_404_NOT_FOUND)

        # Парсинг даты и времени из запроса
        datetime_str = f"{date_str} {time_str}"
        requested_datetime = parse_datetime(datetime_str)

        if not requested_datetime:
            return Response({'error': 'Invalid date or time format'}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.is_naive(requested_datetime):
            requested_datetime = timezone.make_aware(requested_datetime, timezone.get_current_timezone())

        # Время начала и конца бронирования с учётом времени уборки
        start_time = requested_datetime - timedelta(hours=2)  # 2 часа до начала бронирования на уборку
        end_time = requested_datetime + timedelta(hours=booking_duration + 2)  # Длительность бронирования + 2 часа уборки
        print(start_time)
        print(end_time)

        # Проверяем, есть ли бронирования, которые перекрываются с запрашиваемым интервалом времени
        booked_halls = Booked.objects.filter(
            hall=hall,
            book_time__lt=end_time,  # Начало бронирования раньше окончания запрашиваемого времени
            book_time__gte=start_time  # Окончание бронирования позже начала запрашиваемого времени
        )

        if booked_halls.exists():
            return Response({
                'available': False,
                'message': f"{hall.name} is not available at the requested time"
            })

        return Response({
            'available': True,
            'message': f"{hall.name} is available at the requested time"
        })
    

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
