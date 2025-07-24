from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.register(Usuario)
admin.site.register(Psicologo)
admin.site.register(Diario)
admin.site.register(CheckinEmocional)
admin.site.register(MetaTerapeutica)
admin.site.register(FraseMotivacional)
admin.site.register(Notificacao)
class FraseMotivacionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto')


@admin.register(FraseFavorita)
class FraseFavoritaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'frase', 'data_adicionada')
    list_filter = ('usuario',)
    search_fields = ('usuario__username', 'frase__texto')