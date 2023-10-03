from datetime import datetime

from django.views.generic import DetailView

from .filters import SensorReadingFilter
from .models import Sensor


class SensorReadingView(DetailView):
    model = Sensor
    context_object_name = 'sensor'
    template_name = 'sensors/sensor_readings_.html'
    filterset_class = SensorReadingFilter

    @staticmethod
    def qs_to_chart_data(readings):
        data = (
            f'[new Date({int(r.measured_at.timestamp()) * 1000}), {r.value}]'
            for r in readings
        )
        s = ', '.join(data)
        return f'[{s}]'

    @staticmethod
    def qs_to_timeline_data(intervals):
        data = (
            (f"['{i.status}', "
             f"new Date({int(i.started_at.timestamp()) * 1000}), "
             f"new Date({(int((i.finished_at or datetime.now()).timestamp()) * 1000)})]")
            for i in intervals
        )
        s = ', '.join(data)
        return f'[{s}]'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        readings_filter = self.filterset_class(
            self.request.GET,
            queryset=self.object.readings.order_by('measured_at')
        )

        data['readings_filter'] = readings_filter
        data['chart_data'] = self.qs_to_chart_data(readings_filter.qs)
        f = readings_filter.qs[0]
        l = readings_filter.qs[len(readings_filter.qs) - 1]
        data['timeline_data'] = self.qs_to_timeline_data(
            (self
             .object
             .working_intervals
             .filter(finished_at__gt=f.measured_at, started_at__lte=l.measured_at))
        )

        return data
