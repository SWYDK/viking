
from django.contrib import admin
from .models import User, Halls, Foods, Booked, Admins, Goods, Services, Cart, CartFood, CartService, CartGoods,Notify, WebAppData
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.register(User)
admin.site.register(Halls)
admin.site.register(Foods)
admin.site.register(Booked)
admin.site.register(Admins)
admin.site.register(Goods)
admin.site.register(Services)


admin.site.register(Cart)
admin.site.register(CartFood)
admin.site.register(CartService)
admin.site.register(CartGoods)
admin.site.register(Notify)
admin.site.register(WebAppData)






