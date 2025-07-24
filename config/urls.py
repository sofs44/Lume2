from django.contrib import admin
from django.urls import path
from app.views import IndexView, DiarioView, CheckinView, MetasView, LoginView
from app.views import ConteudoView
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('diario/', DiarioView.as_view(), name='diario'),
    path('checkin/', CheckinView.as_view(), name='checkin'),
    path('metas/', MetasView.as_view(), name='metas'),
    path('login/', LoginView.as_view(), name='login'),
    path('conteudo/', ConteudoView.as_view(), name='conteudo'),
    path('notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),
    path('favoritas/', views.minhas_favoritas, name='minhas_favoritas'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

