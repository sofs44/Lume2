from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do usuário")
    email = models.EmailField(max_length=100, unique=True, verbose_name="E-mail do usuário")
    senha = models.CharField(max_length=10, verbose_name="Senha do usuário")
    data_nasc = models.DateField(verbose_name="Data de nascimento")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class Psicologo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do psicólogo")
    email = models.EmailField(max_length=100, unique=True, verbose_name="E-mail do psicólogo")
    registro_crp = models.CharField(max_length=20, verbose_name="Registro CRP")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Psicólogo"
        verbose_name_plural = "Psicólogos"

class Diario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Diário do usuário")
    texto = models.TextField(verbose_name="Texto do diário") 
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return f"Diário de {self.usuario.nome} em {self.data_criacao.date()}"

    class Meta:
        verbose_name = "Registro de Diário"
        verbose_name_plural = "Registros de Diário"

class CheckinEmocional(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Check-in do usuário")
    humor = models.CharField(max_length=50, verbose_name="Humor do usuário") 
    data = models.DateField(auto_now_add=True, verbose_name="Data do check-in")

    def __str__(self):
        return f"{self.humor} em {self.data}"

    class Meta:
        verbose_name = "Check-in Emocional"
        verbose_name_plural = "Check-ins Emocionais"

class MetaTerapeutica(models.Model):
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE, verbose_name="Meta definida pelo psicólogo")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Meta para o usuário")
    descricao = models.CharField(max_length=200, verbose_name="Descrição da meta")
    status = models.CharField(max_length=20, verbose_name="Status da meta")
    data_criacao = models.DateField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return f"Meta de {self.usuario.nome}: {self.descricao}"

    class Meta:
        verbose_name = "Meta Terapêutica"
        verbose_name_plural = "Metas Terapêuticas"

class FraseMotivacional(models.Model):
    texto = models.TextField(verbose_name="Frase motivacional")

    def __str__(self):
        return self.texto[:50]

    class Meta:
        verbose_name = "Frase Motivacional"
        verbose_name_plural = "Frases Motivacionais"

class Notificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensagem = models.CharField(max_length=255)
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario.nome} - {'Lida' if self.lida else 'Não lida'}"
    
class FraseFavorita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    frase = models.ForeignKey('FraseMotivacional', on_delete=models.CASCADE)
    data_adicionada = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.usuario.username} - {self.frase.texto[:30]}'