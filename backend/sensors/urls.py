from django.urls import path

from . import views

app_name = 'sensors'

urlpatterns = [
    path('<int:pk>/readings/',
         views.SensorReadingView.as_view(),
         name='readings')
]
