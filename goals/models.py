from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    prazo = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    TIPO_CHOICES = [
        ('simples', 'Meta simples'),
        ('progresso', 'Meta por progresso'),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='simples'
    )

    unidade = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    quantidade_total = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    quantidade_atual = models.PositiveIntegerField(
        default=0
    )
# Create your models here.
