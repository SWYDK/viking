# Generated by Django 5.0.6 on 2024-09-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_filtersdata_support_remove_cartfood_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presents',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='foods',
        ),
        migrations.RemoveField(
            model_name='user',
            name='goods',
        ),
        migrations.RemoveField(
            model_name='user',
            name='services',
        ),
        migrations.AddField(
            model_name='filtersdata',
            name='compounds',
            field=models.TextField(default='', verbose_name='Состав'),
        ),
        migrations.AddField(
            model_name='user',
            name='data',
            field=models.JSONField(blank=True, null=True, verbose_name='Данные корзины'),
        ),
        migrations.AddField(
            model_name='user',
            name='got_present',
            field=models.BooleanField(default=False, null=True, verbose_name='Получил подарок'),
        ),
        migrations.AlterField(
            model_name='filtersdata',
            name='kitchentypes',
            field=models.TextField(default='', verbose_name='Типы кухни'),
        ),
    ]