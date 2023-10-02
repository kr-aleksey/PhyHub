from rest_framework.generics import CreateAPIView

from sensors.models import SensorReading
from .serializers import SensorReadingSerializer, SensorReadingListSerializer


class SensorReadingsCreateView(CreateAPIView):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingListSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        return super().post(request, *args, **kwargs)
