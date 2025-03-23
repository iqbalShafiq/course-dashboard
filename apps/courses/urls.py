from django.urls import path
from apps.courses.views import CourseListView

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
]
