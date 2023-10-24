from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from sensors.models import Sensor, SensorReading, WorkingInterval
from .filters import WorkingIntervalFilter
from .serializers import (SensorReadingListSerializer,
                          WorkingIntervalCommentSerializer)


class SensorReadingsCreateView(CreateAPIView):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingListSerializer


class WorkingIntervalViewSet(RetrieveModelMixin,
                             UpdateModelMixin,
                             ListModelMixin,
                             GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = WorkingIntervalCommentSerializer
    filterset_class = WorkingIntervalFilter
    queryset = (WorkingInterval
                .objects
                .prefetch_related('sensor', 'status'))

    def get_queryset(self):
        sensor = get_object_or_404(Sensor.objects.all(),
                                   slug=self.kwargs['sensor'])
        return self.queryset.filter(sensor=sensor)
