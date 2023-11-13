# Generated by Django 4.2.4 on 2023-11-13 07:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_alter_statusreason_options_statusreason_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensorstatus',
            old_name='start_value_range',
            new_name='value_from',
        ),
        migrations.RenameField(
            model_name='sensorstatus',
            old_name='stop_value_range',
            new_name='value_to',
        ),
        migrations.AddField(
            model_name='sensorstatus',
            name='duration_from',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='Длительность с'),
        ),
        migrations.AddField(
            model_name='sensorstatus',
            name='duration_to',
            field=models.DurationField(blank=True, null=True, verbose_name='Длительность до'),
        ),
    ]
