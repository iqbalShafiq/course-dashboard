from django.urls import path

from apps.authentications.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
]
