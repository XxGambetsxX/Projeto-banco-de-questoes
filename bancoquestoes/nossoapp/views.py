from django.shortcuts import render
from .models import Questoes


# Create your views here.
def home(request):
    return render(request, "nossoapp/home.html")

def questoes(request):
    questoes = Questoes.objects.all()
    return render(request, "nossoapp/questoes/questoes.html", {"questoes": questoes})

def login(request):
    return render(request, "nossoapp/autenticacao/login.html")

def register(request):
    return render(request, "nossoapp/autenticacao/register.html")
