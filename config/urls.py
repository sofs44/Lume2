# config/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from app import views



from app.views import (
    AuthView, IndexView, DiarioView, criar_diario, DeleteDiarioView,
    EditDiarioView, CheckinView, ConteudoView,
    listar_notificacoes, minhas_favoritas,
    metas_checkin_redirect, metas_usuario, metas_psicologo
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ROTA DE LOGIN/CADASTRO unificada:
    path('', AuthView.as_view(), name='auth'),
    path('logout/', lambda r: (logout(r), redirect('auth'))[1], name='logout'),

    # Demais rotas da sua aplicação:
    path('index/', IndexView.as_view(), name='index'),
    path('diario/', DiarioView.as_view(), name='diario'),
    path('diario/criar/', criar_diario, name='criar_diario'),
    path('delete/<int:id>/', DeleteDiarioView.as_view(), name='delete'),
    path('edit/<int:id>/', EditDiarioView.as_view(), name='edit_diario'),
    path('checkin/', CheckinView.as_view(), name='checkin'),
    path('conteudo/', ConteudoView.as_view(), name='conteudo'),
    path('notificacoes/', listar_notificacoes, name='listar_notificacoes'),
    path('favoritas/', minhas_favoritas, name='minhas_favoritas'),
    path('metas/', metas_checkin_redirect, name='metas'),
    path('metas/usuario/', metas_usuario, name='metas_usuario'),
    path('metas/psicologo/', metas_psicologo, name='metas_psicologo'),

]
