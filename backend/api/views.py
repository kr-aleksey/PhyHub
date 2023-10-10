from rest_framework.generics import CreateAPIView

from sensors.models import SensorReading
from .serializers import SensorReadingListSerializer


class SensorReadingsCreateView(CreateAPIView):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingListSerializer
