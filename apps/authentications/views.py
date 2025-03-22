from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("teacher-list")

        return render(request, "login.html", {"error": "Invalid credentials"})


def logout_view(request):
    logout(request)
    return redirect("login")
