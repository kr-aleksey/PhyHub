from typing import Any

import requests
from django.conf import settings

from exeptions import SensorError


class GetSensorValue:
    """
    Считывание текущих показаний сенсора.
    Работает с сенсорами физических величин
    """
    def __init__(self, url: str):
        self.url = url
        self.timeout = settings.SENSOR_TIMEOUT

    def get_sensor_response(self) -> dict[str, Any]:
        """
        :return: JSON ответ сервера, преобразованный в dict.
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            raise SensorError(f'Ошибка получения показания сенсора. {err}')

    def get(self, name: str):
        """
        Возвращает значение параметра сенсора.
        :param name: Имя параметра.
        :return: Значение, полученное от сенсора.
        """
        try:
            return self.get_sensor_response()[name]
        except KeyError:
            raise SensorError(
                f'Неверный ответ сенсора. Отсутствует параметр {name}'
            )
