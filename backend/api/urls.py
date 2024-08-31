# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, HallsViewSet, FoodsViewSet, BookedViewSet, GoodsViewSet, 
ServicesViewSet, SMSViewSet, CartViewSet, CartServiceViewSet, CartGoodsViewSet, CartFoodViewSet, WebAppDataViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'halls', HallsViewSet)
router.register(r'foods', FoodsViewSet)
router.register(r'booked', BookedViewSet)
router.register(r'goods', GoodsViewSet)
router.register(r'sevices', ServicesViewSet)
router.register(r'sms', SMSViewSet)
router.register(r'cart', CartViewSet)
router.register(r'cartservice', CartServiceViewSet)
router.register(r'cartgoods', CartGoodsViewSet)
router.register(r'cartfoods', CartFoodViewSet)
router.register(r'webappdata', WebAppDataViewSet)




urlpatterns = [
    path('', include(router.urls)),
]
