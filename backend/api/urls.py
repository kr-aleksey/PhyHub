from django.urls import path

from .views import SensorReadingsCreateView, WorkingIntervalCommentView

urlpatterns = [
    path('create_readings/', SensorReadingsCreateView.as_view()),
    path('working_interval/<int:pk>/comment/', WorkingIntervalCommentView.as_view()),
]
