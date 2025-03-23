from django.contrib import admin

from apps.schedules.models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'course', 'start_time', 'end_time')
    list_filter = ('teacher', 'course')
