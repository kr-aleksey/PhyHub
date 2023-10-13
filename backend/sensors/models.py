from datetime import datetime

from django.db import models
from django.db.models import OuterRef
from django.utils import timezone


class WorkingStatus(models.TextChoices):
    IDLE = 'idl', 'Остановка'
    RUN = 'run', 'Работа'


class Sensor(models.Model):
    verbose_name = models.CharField('Полное наименование',
                                    max_length=50)
    name = models.SlugField('Наименование',
                            unique=True,
                            max_length=25)
    is_enabled = models.BooleanField('Включен',
                                     default=False)
    description = models.CharField('Описание',
                                   max_length=100,
                                   blank=True)

    # current_working_interval = models.ForeignKey(
    #     on_delete=models.PROTECT,
    #     blank=True,
    #     null=True,
    #     verbose_name='Текущий рабочий интервал'
    # )

    class Meta:
        verbose_name = 'Сенсор'
        verbose_name_plural = 'Сенсоры'
        ordering = ['verbose_name']

    def __str__(self):
        return self.verbose_name

    @staticmethod
    def get_working_status(value: float) -> WorkingStatus:
        """
        :param value: Показание сенсора.
        :return: Статус сенсора в зависимости от value.
        """
        if value > 0:
            return WorkingStatus.RUN
        return WorkingStatus.IDLE


class WorkingIntervalQueryset(models.QuerySet):

    def check_interval(self,
                       sensor: Sensor,
                       status: WorkingStatus,
                       on_date: datetime):
        """
        Запрашивает из БД текущий рабочий интервал, сравнивает его статус
        с текущим. Если статусы совпадают, возвращает интервал
        без изменений, иначе создает новы интервал с текущим статусом и
        возвращает его.
        :param on_date: Момент времени измерения.
        :param sensor: Сенсор.
        :param status: Текущий статус.
        :return: Рабочий интервал.
        """

        prev_interval = (self
                         .filter(sensor=sensor)
                         .order_by('started_at')
                         .last())
        # если предыдущих интервалов нет создаем новый
        if prev_interval is None:
            return self.create(sensor=sensor,
                               status=status.value,
                               started_at=on_date)
        # если статус не изменился или дата в прошлом, пропускаем
        if (prev_interval.status == status.value
                or prev_interval.started_at >= on_date):
            return prev_interval
        # иначе обновляем старый и создаем новый
        new_interval = self.create(sensor=sensor,
                                   status=status.value,
                                   started_at=on_date)
        prev_interval.finished_at = on_date
        prev_interval.save()
        return new_interval


class WorkingInterval(models.Model):

    sensor = models.ForeignKey(Sensor,
                               on_delete=models.CASCADE,
                               related_name='working_intervals',
                               verbose_name='Сенсор')
    status = models.CharField('Статус',
                              max_length=3,
                              choices=WorkingStatus.choices)
    started_at = models.DateTimeField('С')
    finished_at = models.DateTimeField('До',
                                       blank=True,
                                       null=True)

    objects = WorkingIntervalQueryset.as_manager()

    class Meta:
        verbose_name = 'Рабочий интервал'
        verbose_name_plural = 'Рабочие интервалы'

    def __str__(self):
        date_format = "%d.%m.%y %H:%M:%S"
        started_at = self.started_at.strftime(date_format)
        finished_at = (self.finished_at.strftime(date_format)
                       if self.finished_at is not None
                       else 'текущее время')
        return f'{started_at} - {finished_at}'


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
    value = models.FloatField('Значение')
    measured_at = models.DateTimeField('Дата и время измерения',
                                       default=timezone.now)
    working_interval = models.ForeignKey(WorkingInterval,
                                         on_delete=models.CASCADE,
                                         related_name='readings',
                                         verbose_name='Измерения')

    objects = SensorReadingQuerySet().as_manager()

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-measured_at']

    def __str__(self):
        return str(self.value)
