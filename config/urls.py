from django.urls import path, include
from django.contrib import admin
from app.views import AuthView, IndexView, ConteudoView, CheckinView, DiarioView, criar_diario, DeleteDiarioView, EditDiarioView, listar_notificacoes, metas_checkin_redirect, metas_psicologo, metas_usuario
from django.contrib.auth import views as auth_views
from app.views import marcar_notificacao_lida 
from app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('conteudo/', ConteudoView.as_view(), name='conteudo'),
    path('checkin/', CheckinView.as_view(), name='checkin'),

    path('diario/', DiarioView.as_view(), name='diario'),
    path('diario/criar/', criar_diario, name='criar_diario'),
    path('diario/editar/<int:id>/', EditDiarioView.as_view(), name='edit_diario'),
    path('diario/excluir/<int:id>/', DeleteDiarioView.as_view(), name='delete_diario'),

    path('notificacoes/', listar_notificacoes, name='notificacoes'),
    path('favoritar_frase/', views.favoritar_frase, name='favoritar_frase'),

    path('metas/', metas_checkin_redirect, name='metas'),
    path('metas/psicologo/', metas_psicologo, name='metas_psicologo'),
    path('metas/usuario/', metas_usuario, name='metas_usuario'),
    path('notificacao/lida/<int:notif_id>/', marcar_notificacao_lida, name='notificacao_lida'),
    
]
