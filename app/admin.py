from .models import *
from django.contrib import admin
from .models import (
    Usuario, Psicologo, Diario, CheckinEmocional, MetaTerapeutica,
    FraseMotivacional, Notificacao, FraseFavorita
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'registro_crp')

@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'emocao', 'data_criacao')
    list_filter = ('usuario', 'emocao')
    search_fields = ('titulo', 'conteudo', 'usuario__username')

@admin.register(CheckinEmocional)
class CheckinEmocionalAdmin(admin.ModelAdmin):
    pass

@admin.register(MetaTerapeutica)
class MetaTerapeuticaAdmin(admin.ModelAdmin):
    pass

@admin.register(FraseMotivacional)
class FraseMotivacionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto')

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    pass

@admin.register(FraseFavorita)
class FraseFavoritaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'frase', 'data_adicionada')
    list_filter = ('usuario',)
    search_fields = ('usuario__username', 'frase__texto')
