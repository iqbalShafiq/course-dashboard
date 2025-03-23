from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.authentications.urls")),
    path("", include("apps.teachers.urls")),
    path("", include("apps.courses.urls")),
]
