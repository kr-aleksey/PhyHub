from django.contrib import admin

from .models import Sensor, SensorEndpoint, SensorReading


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enabled', 'endpoint')
    list_filter = ('is_enabled', 'endpoint')
    search_fields = ('name',)
    fields = ('name',
              'endpoint',
              'parameter',
              'type',
              'max_counter_value',
              'is_enabled',
              'description')
    save_as = True


@admin.register(SensorEndpoint)
class SensorEndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'periodicity')
    search_fields = ('name', 'url')
    fields = ('name', 'url', 'periodicity', 'is_enabled', 'description')
    save_as = True


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('measured_at', 'sensor', 'scalar_value', 'counter_value')
    list_filter = ('sensor',)
    date_hierarchy = 'measured_at'
    fields = ('measured_at', 'sensor', 'scalar_value', 'counter_value')
    # readonly_fields = ('measured_at', 'sensor')
    save_as = True
