from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import DayOfWeek, Schedule
from core.views import LoginRequiredMixinView

class ScheduleListView(LoginRequiredMixinView, ListView):
    model = Schedule
    template_name = "schedule_list.html"
    context_object_name = "schedules"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day_choices'] = DayOfWeek.choices
        return context

class ScheduleDetailView(LoginRequiredMixinView, DetailView):
    model = Schedule
    template_name = "schedule_detail.html"
    context_object_name = "schedule"

class DefaultView(View):
    def get(self, request, *args, **kwargs):
        return redirect('schedule-list')
