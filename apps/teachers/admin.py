from django.contrib import admin

from apps.teachers.models import Teacher, TeacherSetting

@admin.register(TeacherSetting)
class TeacherSettingAdmin(admin.ModelAdmin):
    list_display = ('actor', 'role')
    list_filter = ('actor',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "specialization")
    search_fields = ("name",)
