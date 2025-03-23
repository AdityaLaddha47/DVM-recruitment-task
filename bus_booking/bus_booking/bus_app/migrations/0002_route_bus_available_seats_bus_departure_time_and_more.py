# Generated by Django 5.1.7 on 2025-03-22 12:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='available_seats',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bus',
            name='departure_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='bus',
            name='fare',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_count', models.PositiveIntegerField()),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_app.bus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_app.route'),
        ),
    ]
