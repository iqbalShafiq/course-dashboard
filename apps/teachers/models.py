from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from core.models import BaseModel


ROLE_CHOICES = (
    ("user", "User"),
    ("manager", "Manager"),
)


class TeacherSetting(BaseModel):
    actor = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=ROLE_CHOICES, default="user")


class Teacher(BaseModel):
    actor = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_("Full Name"), max_length=100)
    email = models.EmailField(_("Email Address"), unique=True)
    phone = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)
    specialization = models.CharField(_("Specialization"), max_length=100)
    is_active = models.BooleanField(_("Active Status"), default=True)

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_active_schedules(self):
        """Returns all active schedules for this teacher"""
        return self.schedule_set.filter(is_active=True)

    def get_schedule_count(self):
        """Returns count of all schedules for this teacher"""
        return self.schedule_set.count()
