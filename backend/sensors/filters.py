from django_filters.filterset import FilterSet
from django_filters.filters import DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget

from .models import SensorReading


class SensorReadingFilterSet(FilterSet):
    date = DateTimeFromToRangeFilter(
        field_name='measured_at',
        widget=RangeWidget(attrs={'type': 'datetime-local'}))

    class Meta:
        model = SensorReading
        fields = ['sensor', 'date']
        # fields = {
        #     'measured_at': ['gte', 'lte'],
        # }
