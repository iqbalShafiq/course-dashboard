from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

class Course(BaseModel):
    name = models.CharField(_("Course Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True, null=True)
    capacity = models.PositiveIntegerField(_("Capacity"), default=10)
    is_active = models.BooleanField(_("Active Status"), default=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def get_schedules(self):
        """Returns all schedules for this course"""
        return self.schedule_set.all()
    
    def get_active_schedules(self):
        """Returns active schedules for this course"""
        return self.schedule_set.filter(is_active=True)