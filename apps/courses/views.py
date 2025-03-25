from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from apps.courses.models import Course
from apps.courses.forms import CourseEditForm
from apps.teachers.models import TeacherSetting
from core.views import LoginRequiredMixinView
from django.views import View
from django.http import JsonResponse
from apps.courses.tasks import assign_schedules


class CourseListView(LoginRequiredMixinView, ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_settings"] = TeacherSetting.objects.filter(actor=self.request.user).first()
        return context


class CourseDetailView(LoginRequiredMixinView, DetailView):
    model = Course
    template_name = "course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_settings"] = TeacherSetting.objects.filter(actor=self.request.user).first()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        course = self.get_object()

        if action == 'process' and not course.is_task_running():
            assign_schedules(course.id)

        return redirect('course-detail', pk=course.id)

class CourseEditView(LoginRequiredMixinView, UpdateView):
    model = Course
    form_class = CourseEditForm
    template_name = "course_editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_settings"] = TeacherSetting.objects.filter(actor=self.request.user).first()
        return context

    def get_success_url(self):
        return reverse_lazy("course-list")


class CourseCreateView(LoginRequiredMixinView, CreateView):
    model = Course
    form_class = CourseEditForm
    template_name = "course_editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_settings"] = TeacherSetting.objects.filter(actor=self.request.user).first()
        return context

    def get_success_url(self):
        return reverse_lazy("course-list")


class CourseTaskStatusView(LoginRequiredMixinView, View):
    def get(self, request, pk, *args, **kwargs):
        course = Course.objects.get(pk=pk)
        return JsonResponse({"task_running": course.task_running})