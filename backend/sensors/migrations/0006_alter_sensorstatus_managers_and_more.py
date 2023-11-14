# Generated by Django 4.2.4 on 2023-11-13 13:27

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0005_workinginterval_last_reading_value'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='sensorstatus',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='workinginterval',
            name='last_reading_value',
            field=models.FloatField(verbose_name='Крайнее измеренное значение'),
        ),
    ]