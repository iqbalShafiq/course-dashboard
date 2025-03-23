from django.urls import path
from apps.teachers.views import TeacherListView, TeacherEditView

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teacher-list"),
    path("teachers/<str:pk>/edit/", TeacherEditView.as_view(), name="teacher-edit"),
]
