from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("questoes/", views.questoes, name="questoes"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls"))
]

