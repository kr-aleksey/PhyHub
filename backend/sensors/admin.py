from django.contrib import admin

from .models import Sensor, SensorReading, WorkingInterval


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('verbose_name', 'name', 'is_enabled')
    list_filter = ('is_enabled',)
    search_fields = ('verbose_name', 'name')
    fields = ('verbose_name',
              'name',
              'is_enabled',
              'description')
    save_as = True


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('measured_at', 'sensor', 'value')
    list_filter = ('sensor',)
    date_hierarchy = 'measured_at'
    fields = ('measured_at', 'sensor', 'value')
    # readonly_fields = ('measured_at', 'sensor')
    save_as = True


@admin.register(WorkingInterval)
class WorkingIntervalAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'status', 'started_at', 'finished_at')
    list_filter = ('sensor', 'status')
    date_hierarchy = 'started_at'
    fields = ('sensor', 'status', 'started_at', 'finished_at')
    save_as = True
