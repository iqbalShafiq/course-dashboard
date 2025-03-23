from django.views.generic import ListView
from apps.courses.models import Course

class CourseListView(ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(is_active=True)
