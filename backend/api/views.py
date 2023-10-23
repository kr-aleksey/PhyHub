from rest_framework.generics import CreateAPIView, UpdateAPIView

from sensors.models import SensorReading, WorkingInterval
from .serializers import (SensorReadingListSerializer,
                          WorkingIntervalCommentSerializer)


class SensorReadingsCreateView(CreateAPIView):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingListSerializer


class WorkingIntervalCommentView(UpdateAPIView):
    queryset = WorkingInterval.objects.all()
    serializer_class = WorkingIntervalCommentSerializer

