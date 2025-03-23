from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from apps.teachers.forms import TeacherEditForm
from apps.teachers.models import Teacher, TeacherSetting
from core.views import LoginRequiredMixinView


class TeacherListView(LoginRequiredMixinView, ListView):

    model = Teacher
    template_name = "teacher_list.html"
    context_object_name = "teachers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teachers = Teacher.objects.all()
        user_settings = TeacherSetting.objects.filter(actor=self.request.user).first()

        context["teachers"] = teachers
        context["user_settings"] = user_settings
        return context


class TeacherEditView(LoginRequiredMixinView, UpdateView):
    model = Teacher
    form_class = TeacherEditForm
    template_name = "teacher_editor.html"

    def get_success_url(self):
        return reverse_lazy("teacher-list")
