from django.http import HttpResponse
from django.shortcuts import render

from sensors.models import SensorEndpoint


def test_view(request):
    endpoints = SensorEndpoint.objects.prefetch_related('sensors').all()
    for endpoint in endpoints:
        endpoint.update_sensor_readings(
            sensor_values={"s11": {"count": 10},
                           "s10": {"count": 3485211},
                           "s21": {"count": 59003},
                           "s20": {"count": 2670196}}
        )
    return HttpResponse('test')
