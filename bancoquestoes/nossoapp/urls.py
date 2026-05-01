from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("questoes/", views.questoes, name="questoes"),
    path("register/", views.register, name="register"),
    path("registration", views.login, name="login"),
    path("logout/", views.exit, name="logout"),
]
