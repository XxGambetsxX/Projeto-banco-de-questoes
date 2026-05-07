from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("questoes/", views.questoes, name="questoes"),
    path("questoes/<int:questao_id>/responder/", views.responder_questao, name="responder_questao"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login", views.login, name="login"),
    path("logout/", views.exit, name="logout"),
    path("minha-conta/", views.minha_conta, name="minha_conta"),
    path("meu-dia/", views.meu_dia, name="meu_dia"),
]