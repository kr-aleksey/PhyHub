from typing import Any, Optional

import requests
from django.conf import settings
from django.db import IntegrityError

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

    def get_endpoint_response(self) -> dict[str, Any]:
        """
        :return: JSON ответ сервера, преобразованный в dict.
        """
        try:
            response = requests.get(self.endpoint.url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            raise SensorError(f'Ошибка получения показания сенсора. {err}')

    @staticmethod
    def get_sensor_value(response: dict[str, Any],
                         sensor_name: str,
                         parameter_name: str) -> Optional[int]:
        """
        Возвращает значение параметра или None,
        если параметр отсутствует в response.
        :param response: Ответ API
        :param sensor_name: Sensor.name
        :param parameter_name: Sensor.parameter
        :return: Показания сенсора
        """
        try:
            return response.get(sensor_name).get(parameter_name)
        except AttributeError:
            return None

    def create_readings(self) -> Optional[list[SensorReading]]:
        """
        Считывает показания сенсоров и сохраняет в БД.
        """
        if not self.endpoint.is_enabled:
            return None
        sensors = self.endpoint.sensors.filter(is_enabled=True)
        if len(sensors) == 0:
            return None
        response = self.get_endpoint_response()
        # Подготавливаем объекты SensorReading,
        # пропускаем если не получено значение сенсора
        readings = []
        for sensor in sensors:
            sensor_value = self.get_sensor_value(response,
                                                 sensor.name,
                                                 sensor.parameter)
            if sensor_value is not None:
                readings.append(
                    SensorReading(sensor=sensor, value=sensor_value)
                )
        if len(readings) == 0:
            return None

        try:
            return SensorReading.objects.bulk_create(readings)
        except IntegrityError as err:
            raise SensorError(f'Ошибка сохранения показаний сенсора. {err}')
