from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.teachers.models import Teacher
from apps.courses.models import Course
from core.models import BaseModel

class DayOfWeek(models.TextChoices):
    MONDAY = 'monday', _('Monday')
    TUESDAY = 'tuesday', _('Tuesday')
    WEDNESDAY = 'wednesday', _('Wednesday')
    THURSDAY = 'thursday', _('Thursday')
    FRIDAY = 'friday', _('Friday')
    SATURDAY = 'saturday', _('Saturday')
    SUNDAY = 'sunday', _('Sunday')

class Schedule(BaseModel):
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.CASCADE, 
        verbose_name=_("Teacher")
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        verbose_name=_("Course")
    )
    day_of_week = models.CharField(
        _("Day of Week"), 
        max_length=10, 
        choices=DayOfWeek.choices
    )
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))
    room = models.CharField(_("Room"), max_length=50)
    is_active = models.BooleanField(_("Active Status"), default=True)

    class Meta:
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")
        ordering = ["day_of_week", "start_time"]
        # Ensuring no time conflict for teacher
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'day_of_week', 'start_time'],
                name='unique_teacher_timeslot'
            ),
            # Ensuring no time conflict for room
            models.UniqueConstraint(
                fields=['room', 'day_of_week', 'start_time'],
                name='unique_room_timeslot'
            )
        ]

    def __str__(self):
        return f"{self.course.name} - {self.teacher.name} - {self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')}"
    
    def clean(self):
        # Additional validation can be added here
        from django.core.exceptions import ValidationError
        
        if self.start_time >= self.end_time:
            raise ValidationError({
                'end_time': _('End time must be after start time')
            })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def duration_minutes(self):
        """Return the duration of the schedule in minutes"""
        from datetime import datetime
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        
        duration = end_datetime - start_datetime
        return duration.seconds // 60