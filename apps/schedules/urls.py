from django.urls import path
from .views import DefaultView, ScheduleListView, ScheduleDetailView

urlpatterns = [
    path("", DefaultView.as_view(), name="index"),
    path("schedules/", ScheduleListView.as_view(), name="schedule-list"),
    path("schedules/<str:pk>/", ScheduleDetailView.as_view(), name="schedule-detail"),
]
