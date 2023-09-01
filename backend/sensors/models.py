from django.core.validators import MinValueValidator
from django.db import models


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


class Sensor(models.Model):
    ABSOLUTE = 'abs'
    RELATIVE = 'rel'
    TYPES = (
        (ABSOLUTE, 'Абсолютное значение'),
        (RELATIVE, 'Относительное значение'),
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
                            max_length=5)
    is_enabled = models.BooleanField('Включен',
                                     default=False)
    description = models.CharField('Описание',
                                   blank=True)

    class Meta:
        verbose_name = 'Сенсор'
        verbose_name_plural = 'Сенсоры'
        ordering = ['name']

    def __str__(self):
        return self.name


class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor,
                               on_delete=models.CASCADE,
                               related_name='readings',
                               verbose_name='Сенсор')
    value = models.IntegerField('Значение')
    date = models.DateTimeField('Дата',
                                auto_now_add=True)

    class Meta:
        verbose_name = 'Показание сенсора'
        verbose_name_plural = 'Показания сенсоров'
        ordering = ['-date']

    def __str__(self):
        return str(self.value)
