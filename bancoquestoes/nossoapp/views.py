from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from .models import Questoes
from .forms import CadastroForm

# Create your views here.
def home(request):
    return render(request, "nossoapp/home.html")

def register(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "nossoapp/home.html")
    else:
        form = CadastroForm()
    return render(request, "nossoapp/registration/register.html", {"form": form})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("questoes")
        else:
            return render(request, "nossoapp/registration/login.html", {
                "erro": "Usuário ou senha inválidos."
            })

    return render(request, "nossoapp/registration/login.html")

@login_required
def questoes(request):
    questoes = Questoes.objects.prefetch_related("alternativas").all()

    # filtros
    materias = request.GET.getlist("materia")
    dificuldades = request.GET.getlist("dificuldade")

    if materias:
        questoes = questoes.filter(materia__in=materias)

    if dificuldades:
        questoes = questoes.filter(dificuldade__in=dificuldades)

    return render(request, "nossoapp/questoes/questoes.html", {
        "questoes": questoes
    })