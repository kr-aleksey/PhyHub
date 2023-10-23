from django.contrib import admin

from .models import Sensor, SensorStatus


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_enabled')
    list_filter = ('is_enabled',)
    search_fields = ('name', 'slug')
    fields = ('name',
              'slug',
              'is_enabled',
              'description')
    save_as = True


@admin.register(SensorStatus)
class SensorStatusAdmin(admin.ModelAdmin):
    list_display = ('sensor',
                    'name',
                    'start_value_range',
                    'stop_value_range',
                    'color',
                    'need_comment')
    search_fields = ('name', )
    fields = ('sensor',
              'name',
              'start_value_range',
              'stop_value_range',
              'color',
              'need_comment')
    save_as = True
