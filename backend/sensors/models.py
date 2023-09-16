from datetime import datetime
from typing import Any, Optional

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import OuterRef, Q


class SensorEndpoint(models.Model):
    name = models.CharField('Наименование',
                            max_length=25,
                            unique=True)
    url = models.URLField('url')
    periodicity = models.PositiveIntegerField(
        'Периодичность опроса, сек.',
        validators=[MinValueValidator(1)]
    )
    is_enabled = models.BooleanField('Включен',
                                     default=False)
    description = models.CharField('Описание',
                                   blank=True)

    class Meta:
        verbose_name = 'Endpoint'
        verbose_name_plural = 'Endpoints'
        ordering = ['name']

    def __str__(self):
        return self.name

    def update_sensor_readings(self,
                               sensor_values: dict[str, dict[str, Any]]
                               ) -> list:
        if not self.is_enabled:
            return []
        sensors = self.sensors.filter(is_enabled=True)
        # Получаем предыдущие показания для счетчиков
        counter_ids = [s.pk for s in sensors if s.type == s.COUNTER]
        latest_counter_values = {}
        if len(counter_ids) > 0:
            for reading in (SensorReading
                            .objects
                            .filter_latest(sensor_id__in=counter_ids)):
                latest_counter_values[reading.sensor_id] = reading.counter_value
        # Подготавливаем список новых измерений
        new_readings = []
        for sensor in sensors:
            # Получаем новое показание датчика
            try:
                sensor_value = sensor_values[sensor.name][sensor.parameter]
            except (KeyError, TypeError):
                continue
            # Рассчитываем значения
            if sensor.type == Sensor.COUNTER:
                counter_value = sensor_value
                scalar_value = sensor.get_counter_diff(
                    latest_counter_values.get(sensor.pk),
                    counter_value
                )
            else:
                counter_value = None
                scalar_value = sensor_value

            new_readings.append(
                SensorReading(sensor=sensor,
                              scalar_value=scalar_value,
                              counter_value=counter_value)
            )
        if len(new_readings) > 0:
            return SensorReading.objects.bulk_create(new_readings)
        return []


class Sensor(models.Model):
    SCALAR = 'scl'
    COUNTER = 'cnt'
    TYPES = (
        (SCALAR, 'Абсолютное значение'),
        (COUNTER, 'Накопительное значение'),
    )
    endpoint = models.ForeignKey(SensorEndpoint,
                                 on_delete=models.CASCADE,
                                 related_name='sensors',
                                 verbose_name='Endpoint')
    name = models.CharField('Имя',
                            max_length=25,
                            unique=True)
    parameter = models.CharField('Параметр',
                                 max_length=20)
    type = models.CharField('Тип параметра',
                            choices=TYPES,
                            max_length=3)
    max_counter_value = models.PositiveIntegerField('Предел счета',
                                                    blank=True,
                                                    null=True)
    is_enabled = models.BooleanField('Включен',
                                     default=False)
    description = models.CharField('Описание',
                                   blank=True)

    class Meta:
        verbose_name = 'Сенсор'
        verbose_name_plural = 'Сенсоры'
        ordering = ['name']
        constraints = [
            models.CheckConstraint(
                check=(~Q(type='cnt')
                       | (Q(type='cnt') & Q(max_counter_value__isnull=False))),
                name='for_typ_counter_max_counter_value_is_not_null'
            )
        ]

    def __str__(self):
        return self.name

    def get_counter_diff(self,
                         prev_counter_value: Optional[int],
                         counter_value: int) -> int:
        """
        Возвращает разность значений счетчика с учетом возможного переполнения.
        :param prev_counter_value: Предшествующее значение счетчика.
        :param counter_value: Значение счетчика.
        :return: Разность показаний.
        """
        if self.type != self.COUNTER or prev_counter_value is None:
            return 0
        if prev_counter_value > counter_value:
            return self.max_counter_value - prev_counter_value + counter_value
        return counter_value - prev_counter_value


class SensorReadingQuerySet(models.QuerySet):

    def filter_latest(self, **kwargs):
        latest_reading = (self
                          .filter(sensor=OuterRef('sensor'))
                          .order_by('-measured_at')
                          .values('pk')[:1])
        return self.filter(pk=latest_reading, **kwargs)


class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor,
                               on_delete=models.CASCADE,
                               related_name='readings',
                               verbose_name='Сенсор')
    scalar_value = models.IntegerField('Значение')
    counter_value = models.IntegerField('Показание счетчика',
                                        blank=True,
                                        null=True)
    measured_at = models.DateTimeField('Дата и время измерения',
                                       default=datetime.now)

    objects = SensorReadingQuerySet().as_manager()

    class Meta:
        verbose_name = 'Показание сенсора'
        verbose_name_plural = 'Показания сенсоров'
        ordering = ['-measured_at']

    def __str__(self):
        return str(self.scalar_value)
