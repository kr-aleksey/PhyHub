from django.db.models import BooleanField, F, Max, Min, Value
from django.db.models.functions import Cast, Greatest
from django_filters.views import FilterView

from .filters import SensorReadingFilterSet
from .models import SensorReading


class SensorReadingView(FilterView):
    model = SensorReading
    filterset_class = SensorReadingFilterSet
    template_name = 'sensors/sensor_readings.html'

    def get_queryset(self):
        qs = (self
              .model
              .objects
              .order_by('measured_at'))

        print(qs.query)
        return qs
