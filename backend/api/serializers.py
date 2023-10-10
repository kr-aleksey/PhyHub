from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sensors.models import Sensor, SensorReading, WorkingInterval


class SensorReadingSerializer(serializers.ModelSerializer):
    sensor = serializers.SlugField()

    class Meta:
        model = SensorReading
        fields = ['sensor', 'value', 'measured_at']
        read_only_fields = ['measured_at']


class SensorReadingListSerializer(serializers.ListSerializer):
    child = SensorReadingSerializer()

    def create(self, validated_data):
        """
        Создает объекты SensorReading в БД. Игнорирует данные сенсоров
        с атрибутом is_enabled == False
        """
        measured_at = timezone.now()
        sensors = (Sensor
                   .objects
                   .filter(name__in={i['sensor'] for i in validated_data})
                   .in_bulk(field_name='name'))

        readings = []
        errors = []
        for data in validated_data:
            name = data['sensor']
            sensor: Sensor = sensors.get(name)
            if sensor is None:
                errors.append(f'Не найден сенсор {name}')
            elif sensor.is_enabled:
                interval = WorkingInterval.objects.check_interval(
                    sensor=sensor,
                    status=sensor.get_working_status(data['value']),
                    on_date=measured_at
                )
                data['sensor'] = sensor
                data['measured_at'] = measured_at
                data['working_interval'] = interval
                readings.append(SensorReading(**data))

        if errors:
            raise ValidationError(errors)

        return SensorReading.objects.bulk_create(readings)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
