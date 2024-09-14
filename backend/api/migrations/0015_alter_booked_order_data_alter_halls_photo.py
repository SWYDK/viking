# Generated by Django 5.0.6 on 2024-09-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_remove_presents_user_remove_user_foods_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booked',
            name='order_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='halls',
            name='photo',
            field=models.JSONField(default=list, verbose_name='Фото зала'),
        ),
    ]
