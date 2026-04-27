from django.shortcuts import render, HttpResponse
from .models import Questoes

# Create your views here.
def home(request):
    return render(request, "home.html")

def questoes(request):
    questoes = Questoes.objects.all()
    return render(request, "questoes.html", {"questoes": questoes})

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")
