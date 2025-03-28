from django.urls import path
from apps.courses.views import CourseDetailView, CourseListView, CourseEditView, CourseCreateView, CourseTaskStatusView

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("courses/<str:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("courses/<str:pk>/edit/", CourseEditView.as_view(), name="course-edit"),
    path("courses/create/new", CourseCreateView.as_view(), name="create-courses"),
    path('course/<str:pk>/task-status/', CourseTaskStatusView.as_view(), name='course-task-status'),
]
