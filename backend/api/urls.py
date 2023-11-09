from django.urls import path

from .views import (SensorReadingsCreateView, WorkingIntervalViewSet)

urlpatterns = [
    path('create_readings/',
         SensorReadingsCreateView.as_view(),
         name='create_sensor_readings'),

    path('sensors/<str:sensor_slug>/intervals/',
         WorkingIntervalViewSet.as_view({'get': 'list'}),
         name='working_intervals_list'),

    path('sensors/<str:sensor_slug>/intervals/<int:interval_pk>/',
         WorkingIntervalViewSet.as_view({
             'get': 'retrieve',
             'patch': 'partial_update',
         }),
         name='working_interval'),
]
