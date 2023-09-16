# Generated by Django 4.2.4 on 2023-09-15 11:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True, verbose_name='Имя')),
                ('parameter', models.CharField(max_length=20, verbose_name='Параметр')),
                ('type', models.CharField(choices=[('scl', 'Абсолютное значение'), ('cnt', 'Относительное значение')], max_length=3, verbose_name='Тип параметра')),
                ('max_counter_value', models.PositiveIntegerField(blank=True, null=True, verbose_name='Предел счета')),
                ('is_enabled', models.BooleanField(default=False, verbose_name='Включен')),
                ('description', models.CharField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Сенсор',
                'verbose_name_plural': 'Сенсоры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SensorEndpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True, verbose_name='Наименование')),
                ('url', models.URLField(verbose_name='url')),
                ('periodicity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Периодичность опроса, сек.')),
                ('is_enabled', models.BooleanField(default=False, verbose_name='Включен')),
                ('description', models.CharField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Endpoint',
                'verbose_name_plural': 'Endpoints',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scalar_value', models.IntegerField(verbose_name='Значение')),
                ('counter_value', models.IntegerField(blank=True, null=True, verbose_name='Показание счетчика')),
                ('measured_at', models.DateTimeField(verbose_name='Дата и время измерения')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='sensors.sensor', verbose_name='Сенсор')),
            ],
            options={
                'verbose_name': 'Показание сенсора',
                'verbose_name_plural': 'Показания сенсоров',
                'ordering': ['-measured_at'],
            },
        ),
        migrations.AddField(
            model_name='sensor',
            name='endpoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensors', to='sensors.sensorendpoint', verbose_name='Endpoint'),
        ),
        migrations.AddConstraint(
            model_name='sensor',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('type', 'cnt'), _negated=True), models.Q(('type', 'cnt'), ('max_counter_value__isnull', False)), _connector='OR'), name='for_typ_counter_max_counter_value_is_not_null'),
        ),
    ]
