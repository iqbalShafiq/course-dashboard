from django.urls import path

from apps.teachers.views import TeacherListView

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teacher-list"),
]
