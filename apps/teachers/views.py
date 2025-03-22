from django.shortcuts import render
from django.views.generic import ListView
from apps.teachers.models import Teacher
from core.views import LoginRequiredMixinView


class TeacherListView(LoginRequiredMixinView, ListView):

    model = Teacher
    template_name = "teacher_list.html"
    context_object_name = "teachers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teachers = Teacher.objects.all()

        context["teachers"] = teachers
        return context
