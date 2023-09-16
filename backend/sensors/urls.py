from django.urls import path

from . import views

app_name = 'sensors'

urlpatterns = [
    path('test/', views.test_view)
]
