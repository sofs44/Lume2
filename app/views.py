from django.shortcuts import render
from django.views import View
from .models import FraseMotivacional, Diario, CheckinEmocional, MetaTerapeutica
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Notificacao
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import (
    FraseMotivacional,
    Diario,
    CheckinEmocional,
    MetaTerapeutica,
    Notificacao,
    FraseFavorita,
)

class IndexView(View):
    def get(self, request, *args, **kwargs):
        frase_aleatoria = FraseMotivacional.objects.order_by('?').first()
        if frase_aleatoria:
            texto_frase = frase_aleatoria.texto
        else:
            texto_frase = "Seja bem-vindo ao Lume!"

        return render(request, 'index.html', {"frase": texto_frase})


class DiarioView(View):
    def get(self, request, *args, **kwargs):
        diarios = Diario.objects.all()
        return render(request, 'diario.html', {'diarios': diarios})


class CheckinView(View):
    def get(self, request, *args, **kwargs):
        checkins = CheckinEmocional.objects.all()
        return render(request, 'checkin.html', {'checkins': checkins})


class MetasView(View):
    def get(self, request, *args, **kwargs):
        metas = MetaTerapeutica.objects.all()
        return render(request, 'metas.html', {'metas': metas})

class ConteudoView(View):
    template_name = 'conteudo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        senha = request.POST['senha']
        usuario = authenticate(request, username=username, password=senha)

        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'login.html')

@login_required
def listar_notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, 'notificacoes.html', {'notificacoes': notificacoes})

@login_required
def minhas_favoritas(request):
    favoritas = FraseFavorita.objects.filter(usuario=request.user)
    return render(request, 'favoritas.html', {'favoritas': favoritas})