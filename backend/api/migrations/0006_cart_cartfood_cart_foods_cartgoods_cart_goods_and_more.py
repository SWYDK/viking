# Generated by Django 5.0.6 on 2024-08-26 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_sms_code_from_user_halls_desc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_time', models.DateTimeField(verbose_name='Время бронирования')),
                ('booking_time', models.IntegerField(verbose_name='Количество забронированных часов')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.halls')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='CartFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.foods')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='foods',
            field=models.ManyToManyField(blank=True, related_name='cart_bookings', through='api.CartFood', to='api.foods'),
        ),
        migrations.CreateModel(
            name='CartGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.goods')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='goods',
            field=models.ManyToManyField(blank=True, related_name='cart_bookings', through='api.CartGoods', to='api.goods'),
        ),
        migrations.CreateModel(
            name='CartService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.services')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='cart_bookings', through='api.CartService', to='api.services'),
        ),
    ]