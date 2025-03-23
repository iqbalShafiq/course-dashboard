from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from apps.courses.models import Course
from apps.courses.forms import CourseEditForm
from core.views import LoginRequiredMixinView
from django.shortcuts import render


class CourseListView(LoginRequiredMixinView, ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(is_active=True)


class CourseDetailView(LoginRequiredMixinView, DetailView):
    model = Course
    template_name = "course_detail.html"
    context_object_name = "course"


class CourseEditView(LoginRequiredMixinView, UpdateView):
    model = Course
    form_class = CourseEditForm
    template_name = "course_editor.html"

    def get_success_url(self):
        return reverse_lazy("course-list")


class CourseCreateView(LoginRequiredMixinView, CreateView):
    model = Course
    form_class = CourseEditForm
    template_name = "course_editor.html"

    def get_success_url(self):
        return reverse_lazy("course-list")
