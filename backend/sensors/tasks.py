from celery import shared_task

from PhyHub.celery import app
from .exeptions import SensorError
from .models import SensorEndpoint
from .services import SensorReadingsService


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Создаем периодические задачи для каждого endpoint-а.
    """
    endpoints = SensorEndpoint.objects.prefetch_related('sensors').all()
    for endpoint in endpoints:
        sender.add_periodic_task(
            endpoint.periodicity,
            create_sensor_readings_task.s(endpoint_id=endpoint.pk)
        )


@shared_task()
def create_sensor_readings_task(endpoint_id: int):
    """
    Получает показания всех сенсоров endpoint-а, сохраняет в БД.
    :param endpoint_id: SensorEndpoint.pk
    """
    try:
        SensorReadingsService(endpoint_id).update_readings()
    except SensorError:
        pass
