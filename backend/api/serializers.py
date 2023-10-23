from django.utils import timezone
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
                   .filter(slug__in={i['sensor'] for i in validated_data})
                   .in_bulk(field_name='slug'))

        readings = []
        errors = []
        for reading_data in validated_data:
            slug = reading_data['sensor']
            sensor: Sensor = sensors.get(slug)
            if sensor is None:
                errors.append(f'Не найден сенсор {slug}')
            elif sensor.is_enabled:
                interval = WorkingInterval.objects.check_interval(
                    sensor=sensor,
                    status=sensor.get_working_status(reading_data['value']),
                    on_date=measured_at
                )
                reading_data['sensor'] = sensor
                reading_data['measured_at'] = measured_at
                reading_data['working_interval'] = interval
                readings.append(SensorReading(**reading_data))

        if errors:
            raise ValidationError(errors)

        return SensorReading.objects.bulk_create(readings)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)


class WorkingIntervalCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkingInterval
        fields = ['comment']
