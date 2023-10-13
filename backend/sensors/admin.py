from django.contrib import admin

from .models import Sensor


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
