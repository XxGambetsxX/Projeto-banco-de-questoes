from django.shortcuts import render, HttpResponse
from .models import Questao

# Create your views here.
def home(request):
    return render(request, "home.html")

def questoes(request):
    questoes = Questao.objects.all()
    return render(request, "questoes.html", {"questoes": questoes})
