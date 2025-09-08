# app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .models import (
    Psicologo, Usuario, FraseMotivacional, Diario, CheckinEmocional,
    MetaTerapeutica, Notificacao, FraseFavorita
)
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


# ----------------- FORMULÁRIOS -----------------

class DiarioForm(forms.ModelForm):
    class Meta:
        model = Diario
        fields = ['titulo', 'conteudo', 'emocao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    tipo = forms.ChoiceField(
        label="Sou",
        choices=Usuario.TIPO_CHOICES,
        widget=forms.RadioSelect
    )

    def clean(self):
        cd = super().clean()
        user = authenticate(username=cd.get('username'), password=cd.get('password'))
        if not user:
            raise forms.ValidationError("Usuário ou senha inválidos.")
        try:
            perfil = user.usuario
        except Usuario.DoesNotExist:
            raise forms.ValidationError("Perfil de usuário não encontrado.")
        cd['user_obj'] = user
        return cd

class CadastroForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    nome = forms.CharField(label="Nome completo")
    email = forms.EmailField(label="E-mail")
    data_nasc = forms.DateField(label="Data de nascimento", widget=forms.DateInput(attrs={'type': 'date'}))
    tipo = forms.ChoiceField(label="Sou", choices=Usuario.TIPO_CHOICES, widget=forms.RadioSelect)
    codigo = forms.CharField(label="Código (só psicólogos)", required=False)

    def clean(self):
        cd = super().clean()
        if cd['tipo'] == 'psicologo' and cd.get('codigo') != 'PSICO2024':
            raise forms.ValidationError("Código inválido para psicólogos.")
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError("Usuário já existe.")
        if Usuario.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return cd

# ----------------- AUTH -----------------
@method_decorator(csrf_protect, name='dispatch')
class AuthView(View):
    def get(self, request):
        return render(request, 'auth.html', {
            'login_form': LoginForm(),
            'cadastro_form': CadastroForm()
        })

    def post(self, request):
        # LOGIN
        if 'btn-login' in request.POST:
            login_form = LoginForm(request.POST)
            cadastro_form = CadastroForm()
            if login_form.is_valid():
                user = login_form.cleaned_data['user_obj']
                login(request, user)
                return redirect('index')
            return render(request, 'auth.html', {
                'login_form': login_form,
                'cadastro_form': cadastro_form
            })

        # CADASTRO
        if 'btn-cadastro' in request.POST:
            cadastro_form = CadastroForm(request.POST)
            login_form = LoginForm()
            if cadastro_form.is_valid():
                cd = cadastro_form.cleaned_data
                user = User.objects.create_user(username=cd['username'], password=cd['password'])
                perfil = Usuario.objects.create(
                    user=user,
                    nome=cd['nome'],
                    email=cd['email'],
                    data_nasc=cd['data_nasc'],
                    tipo=cd['tipo']
                )
                if cd['tipo'] == 'psicologo':
                    psicologo = Psicologo.objects.create(
                        nome=cd['nome'],
                        email=cd['email'],
                        registro_crp=cd.get('codigo', '')
                    )
                    perfil.psicologo = psicologo
                    perfil.save()

                login(request, user)
                messages.success(request, "Cadastro realizado com sucesso! Você já está logado.")
                return redirect('index')

            return render(request, 'auth.html', {
                'login_form': login_form,
                'cadastro_form': cadastro_form
            })

# ----------------- VIEWS PRINCIPAIS -----------------

class IndexView(View):
    def get(self, request):
        frase = FraseMotivacional.objects.order_by('?').first()
        return render(request, 'index.html', {
            "frase": frase.texto if frase else "Seja bem-vindo ao Lume!"
        })

@method_decorator(login_required, name='dispatch')
class DiarioView(View):
    def get(self, request):
        diarios = Diario.objects.all().order_by('-data_criacao')
        return render(request, 'diario.html', {'diarios': diarios, 'data_hoje': now().date()})

class CheckinView(View):
    def get(self, request):
        checkins = CheckinEmocional.objects.all()
        return render(request, 'checkin.html', {'checkins': checkins})

class ConteudoView(View):
    def get(self, request):
        return render(request, 'conteudo.html')

# ----------------- FUNÇÕES -----------------

@login_required
def criar_diario(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('texto')
        emocao = request.POST.get('emoji')
        usuario = Usuario.objects.get(user=request.user)
        Diario.objects.create(usuario=usuario, titulo=titulo, conteudo=conteudo, emocao=emocao)
        return redirect('diario')
    return redirect('diario')

@login_required
def listar_notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario__user=request.user).order_by('-data_criacao')
    return render(request, 'notificacoes.html', {'notificacoes': notificacoes})

@login_required
def minhas_favoritas(request):
    favoritas = FraseFavorita.objects.filter(usuario__user=request.user)
    return render(request, 'favoritas.html', {'favoritas': favoritas})

class DeleteDiarioView(View):
    def get(self, request, id):
        get_object_or_404(Diario, id=id).delete()
        messages.success(request, 'Registro excluído com sucesso!')
        return redirect('diario')

class EditDiarioView(View):
    def get(self, request, id):
        form = DiarioForm(instance=get_object_or_404(Diario, id=id))
        return render(request, 'editar_diario.html', {'form': form})
    def post(self, request, id):
        diario = get_object_or_404(Diario, id=id)
        form = DiarioForm(request.POST, instance=diario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado com sucesso!')
            return redirect('diario')
        return render(request, 'editar_diario.html', {'form': form})

# ----------------- METAS -----------------

@login_required
def metas_checkin_redirect(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    if usuario.tipo == 'psicologo':
        return redirect('metas_psicologo')
    return redirect('metas_usuario')

def somente_psicologo(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'usuario') or request.user.usuario.tipo != 'psicologo':
            messages.error(request, "Acesso negado.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@somente_psicologo
def metas_psicologo(request):
    perfil = request.user.usuario
    psicologo_obj = getattr(perfil, 'psicologo', None)
    if psicologo_obj is None:
        psicologo_obj = Psicologo.objects.filter(email=perfil.email).first()
        if psicologo_obj is None:
            messages.error(request, "Perfil de psicólogo não encontrado no sistema.")
            return redirect('index')

    usuarios = Usuario.objects.filter(tipo='usuario').order_by('nome')
    metas = MetaTerapeutica.objects.filter(psicologo=psicologo_obj).order_by('-data_criacao')

    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        status = request.POST.get('status', 'aberta')
        target = request.POST.get('usuario_id')

        if not descricao:
            messages.error(request, "Descrição vazia.")
            return redirect('metas_psicologo')

        if target == 'all':
            for u in usuarios:
                MetaTerapeutica.objects.create(psicologo=psicologo_obj, usuario=u, descricao=descricao, status=status)
            messages.success(request, "Meta criada para todos os usuários.")
        else:
            try:
                u = Usuario.objects.get(id=int(target))
                MetaTerapeutica.objects.create(psicologo=psicologo_obj, usuario=u, descricao=descricao, status=status)
                messages.success(request, f"Meta criada para {u.nome}.")
            except (Usuario.DoesNotExist, ValueError):
                messages.error(request, "Usuário selecionado inválido.")

        return redirect('metas_psicologo')

    return render(request, 'metas_psicologo.html', {'usuarios': usuarios, 'metas': metas})

@login_required
def metas_usuario(request):
    perfil = request.user.usuario
    metas = MetaTerapeutica.objects.filter(usuario=perfil).order_by('-data_criacao')

    if request.method == 'POST' and 'marcar_concluida' in request.POST:
        meta_id = request.POST.get('meta_id')
        try:
            meta = MetaTerapeutica.objects.get(id=meta_id, usuario=perfil)
            meta.status = 'concluida'
            meta.save()
            messages.success(request, "Meta marcada como concluída.")
        except MetaTerapeutica.DoesNotExist:
            messages.error(request, "Meta inválida.")
        return redirect('metas_usuario')

    return render(request, 'metas_usuario.html', {'metas': metas})
