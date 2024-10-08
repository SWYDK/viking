# Generated by Django 5.0.6 on 2024-08-29 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_notify_options_remove_booked_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebAppData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_data', models.JSONField()),
                ('is_viewed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Данные',
                'verbose_name_plural': 'Данные',
            },
        ),
    ]
