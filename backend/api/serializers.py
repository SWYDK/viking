from rest_framework import serializers
from .models import (User, Halls, Foods, Booked, Services, Goods, SMS, 
Cart, CartFood, CartService, CartGoods,WebAppData)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class HallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Halls
        fields = '__all__'


class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = '__all__'


class BookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booked
        fields = '__all__'


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
        
class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMS
        fields = '__all__'


class CartFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartFood
        fields = '__all__'

class CartServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartService
        fields = '__all__'

class CartGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartGoods
        fields = '__all__'

class WebAppDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebAppData
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    foods = CartFoodSerializer(many=True, read_only=True)
    services = CartServiceSerializer(many=True, read_only=True)
    goods = CartGoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'