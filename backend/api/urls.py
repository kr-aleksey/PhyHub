from django.urls import path

from .views import SensorReadingsCreateView

urlpatterns = [
    path('create_readings/', SensorReadingsCreateView.as_view())
]
