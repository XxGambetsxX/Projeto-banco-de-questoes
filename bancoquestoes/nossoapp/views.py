from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Questoes, Alternativa, QuestaoFeita, Estudantes
from .forms import CadastroForm
from datetime import date
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def home(request):
    if not request.user.is_authenticated:
        return render(request, "nossoapp/home.html")

    ano_atual = date.today().year

    questoes_feitas = QuestaoFeita.objects.filter(
        usuario=request.user,
        data__year=ano_atual
    )

    total_resolvidas = questoes_feitas.count()
    total_acertos = questoes_feitas.filter(acertou=True).count()
    total_erros = total_resolvidas - total_acertos

    historico = (
        questoes_feitas
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    meses = [h['mes'].strftime('%b') for h in historico]
    totais = [h['total'] for h in historico]

    return render(request, "nossoapp/home.html", {
        "user": request.user,
        "total_resolvidas": total_resolvidas,
        "total_acertos": total_acertos,
        "total_erros": total_erros,
        "meses": meses,
        "totais": totais,
        "ano_atual": ano_atual,
    })


def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "nossoapp/home.html")
    else:
        form = CadastroForm()
    return render(request, "nossoapp/login/cadastro.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("questoes")
        else:
            return render(
                request,
                "nossoapp/login/login.html",
                {"erro": "Usuário ou senha inválidos."},
            )

    return render(request, "nossoapp/login/login.html")


def exit(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def questoes(request):
    lista_questoes = Questoes.objects.prefetch_related("alternativas").all()

    materias = request.GET.getlist("materia")
    niveis = request.GET.getlist("nivel")
    finalizado = request.GET.get("finalizado", False)

    if materias:
        lista_questoes = lista_questoes.filter(materia__in=materias)
    if niveis:
        lista_questoes = lista_questoes.filter(nivel__in=niveis)

    indice = int(request.GET.get("indice", 0))
    total = lista_questoes.count()

    if indice >= total:
        indice = total - 1
    if indice < 0:
        indice = 0

    questao_atual = lista_questoes[indice] if total > 0 else None

    acertos = None
    if finalizado:
        acertos = QuestaoFeita.objects.filter(
            usuario=request.user,
            questao__in=lista_questoes,
            acertou=True
        ).count()

    return render(request, "nossoapp/questoes/questoes.html", {
        "questao": questao_atual,
        "indice": indice,
        "total": total,
        "materias_ativas": materias,
        "niveis_ativos": niveis,
        "finalizado": finalizado,
        "acertos": acertos,
    })


@login_required(login_url="login")
def responder_questao(request, questao_id):
    if request.method == 'POST':
        alternativa_id = request.POST.get('alternativa')
        indice = int(request.POST.get('indice', 0))
        materias = request.POST.getlist('materia')
        niveis = request.POST.getlist('nivel')

        questao = get_object_or_404(Questoes, id=questao_id)
        alternativa = get_object_or_404(Alternativa, id=alternativa_id, questao=questao)

        QuestaoFeita.objects.create(
            usuario=request.user,
            questao=questao,
            alternativa_escolhida=alternativa
        )

        lista_questoes = Questoes.objects.all()
        if materias:
            lista_questoes = lista_questoes.filter(materia__in=materias)
        if niveis:
            lista_questoes = lista_questoes.filter(nivel__in=niveis)

        params = ""
        for m in materias:
            params += f"&materia={m}"
        for n in niveis:
            params += f"&nivel={n}"

        if indice + 1 >= lista_questoes.count():
            return redirect(f'/questoes/?finalizado=1{params}')

        return redirect(f'/questoes/?indice={indice + 1}{params}')

    return redirect('questoes')


from django.contrib.auth import update_session_auth_hash

@login_required(login_url="login")
def minha_conta(request):
    user = request.user
    estudante = Estudantes.objects.get(usuario=user)
    sucesso = None
    erro = None

    if request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "email":
            email = request.POST.get("email")
            user.email = email
            user.save()
            sucesso = "E-mail atualizado com sucesso!"

        elif acao == "senha":
            senha_atual = request.POST.get("senha_atual")
            nova_senha = request.POST.get("nova_senha")
            confirmar_senha = request.POST.get("confirmar_senha")

            if not user.check_password(senha_atual):
                erro = "Senha atual incorreta."
            elif nova_senha != confirmar_senha:
                erro = "As senhas não coincidem."
            else:
                try:
                    validate_password(nova_senha, user)
                    user.set_password(nova_senha)
                    user.save()
                    update_session_auth_hash(request, user)
                    sucesso = "Senha atualizada com sucesso!"
                except ValidationError as e:
                    erro = " ".join(e.messages)

        elif acao == "foto":
            if request.FILES.get("foto"):
                estudante.foto = request.FILES["foto"]
                estudante.save()
                sucesso = "Foto atualizada com sucesso!"

        elif acao == "username":
            novo_username = request.POST.get("username")
            if User.objects.filter(username=novo_username).exclude(pk=user.pk).exists():
                erro = "Este nome de usuário já está em uso."
            else:
                user.username = novo_username
                user.save()
                sucesso = "Nome de usuário atualizado com sucesso!"

    return render(request, "nossoapp/minha_conta/minha_conta.html", {
        "user": user,
        "estudante": estudante,
        "sucesso": sucesso,
        "erro": erro,
    })


@login_required(login_url="login")
def meu_dia(request):
    hoje = date.today()
    MATERIAS = [('MAT','Matemática'),('LIN','Linguagens'),('HUM','Ciências Humanas'),('NAT','Ciências da Natureza')]
    NIVEIS   = [('F','Fácil'),('M','Médio'),('D','Difícil')]

    qs = QuestaoFeita.objects.filter(usuario=request.user, data__date=hoje)

    total     = qs.count()
    acertos   = qs.filter(acertou=True).count()
    erros     = qs.filter(acertou=False).count()

    dados = []
    for cod, nome in MATERIAS:
        niveis = []
        for ncod, nnome in NIVEIS:
            sub = qs.filter(questao__materia=cod, questao__nivel=ncod)
            a = sub.filter(acertou=True).count()
            e = sub.filter(acertou=False).count()
            niveis.append({'nome': nnome, 'acertos': a, 'erros': e})
        mat_qs = qs.filter(questao__materia=cod)
        a_mat  = mat_qs.filter(acertou=True).count()
        e_mat  = mat_qs.filter(acertou=False).count()
        if a_mat + e_mat > 0:
            dados.append({'nome': nome, 'acertos': a_mat, 'erros': e_mat, 'niveis': niveis})

    return render(request, "nossoapp/meu_dia/meu_dia.html", {
        "hoje": hoje,
        "total": total,
        "acertos": acertos,
        "erros": erros,
        "dados": dados,
    })