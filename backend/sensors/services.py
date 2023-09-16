from typing import Any

import requests
from django.conf import settings

from .exeptions import SensorError
from .models import SensorEndpoint, SensorReading


class SensorReadingsService:
    """
    Считывание текущих показаний сенсора.
    """

    def __init__(self, endpoint_id):
        try:
            self.endpoint = SensorEndpoint.objects.get(pk=endpoint_id)
        except SensorEndpoint.DoesNotExist:
            raise SensorError(f'Не найден endpoint c id={endpoint_id}')
        self.timeout = settings.SENSOR_TIMEOUT

    @property
    def endpoint_response(self) -> dict[str, Any]:
        """
        :return: JSON ответ сервера, преобразованный в dict.
        """
        try:
            response = requests.get(self.endpoint.url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            raise SensorError(f'Ошибка получения показания сенсора. {err}')

    def update_readings(self) -> list[SensorReading]:
        """
        Считывает показания сенсоров и сохраняет в БД.
        """
        return self.endpoint.update_sensor_readings(self.endpoint_response)
