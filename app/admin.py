from django.contrib import admin
from .models import (
    Usuario, Psicologo, Diario, CheckinEmocional, MetaTerapeutica,
    FraseMotivacional, Notificacao, FraseFavorita
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'tipo')
    search_fields = ('nome', 'email')


@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'registro_crp')
    search_fields = ('nome', 'email')


@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'emocao', 'data_criacao')
    list_filter = ('usuario', 'emocao')
    search_fields = ('titulo', 'conteudo', 'usuario__nome')


@admin.register(CheckinEmocional)
class CheckinEmocionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'humor', 'data')
    list_filter = ('data',)
    search_fields = ('usuario__nome', 'humor')


@admin.register(FraseMotivacional)
class FraseMotivacionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto')


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('id_notificacao', 'usuario', 'meta', 'lida', 'data_criacao')
    list_filter = ('lida', 'data_criacao')
    search_fields = ('usuario__nome', 'mensagem')


class NotificacaoInline(admin.TabularInline):
    model = Notificacao
    extra = 1


@admin.register(MetaTerapeutica)
class MetaTerapeuticaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'usuario', 'psicologo', 'status', 'data_criacao')
    list_filter = ('status', 'data_criacao')
    search_fields = ('descricao', 'usuario__nome', 'psicologo__nome')
    inlines = [NotificacaoInline]


@admin.register(FraseFavorita)
class FraseFavoritaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'frase', 'data_adicionada')
    list_filter = ('usuario',)
    search_fields = ('usuario__username', 'frase__texto')
