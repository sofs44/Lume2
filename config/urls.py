from django.urls import path
from .views import AuthView, IndexView, ConteudoView, CheckinView, DiarioView, criar_diario, DeleteDiarioView, EditDiarioView, listar_notificacoes, minhas_favoritas, metas_checkin_redirect, metas_psicologo, metas_usuario

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('', include('app.urls')),
    path('conteudo/', ConteudoView.as_view(), name='conteudo'),
    path('checkin/', CheckinView.as_view(), name='checkin'),

    path('diario/', DiarioView.as_view(), name='diario'),
    path('diario/criar/', criar_diario, name='criar_diario'),
    path('diario/<int:id>/delete/', DeleteDiarioView.as_view(), name='delete_diario'),
    path('diario/<int:id>/edit/', EditDiarioView.as_view(), name='edit_diario'),

    path('notificacoes/', listar_notificacoes, name='notificacoes'),
    path('favoritas/', minhas_favoritas, name='favoritas'),

    path('metas/', metas_checkin_redirect, name='metas'),
    path('metas/psicologo/', metas_psicologo, name='metas_psicologo'),
    path('metas/usuario/', metas_usuario, name='metas_usuario'),
]
