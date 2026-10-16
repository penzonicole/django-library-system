from django.db import models
from django.utils import timezone
from datetime import date

class Autor(models.Model):
    nome = models.CharField(max_length=150)
    nacionalidade = models.CharField(max_length=80, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros')
    isbn = models.CharField(max_length=20, unique=True)
    copias_totais = models.PositiveIntegerField(default=1)
    copias_disponiveis = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.titulo


class Membro(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('DEVOLVIDO', 'Devolvido'),
        ('ATRASADO', 'Atrasado'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_prevista_devolucao = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO')

    @property
    def esta_atrasado(self):
        if self.status == 'DEVOLVIDO':
            return False
        return self.data_prevista_devolucao < timezone.now().date()

    @property
    def valor_multa(self):
        """Calcula R$ 2,00 por dia de atraso (Desafio Multa por Atraso)"""
        VALOR_DIARIO = 2.00
        if self.status == 'DEVOLVIDO' and self.data_devolucao:
            if self.data_devolucao > self.data_prevista_devolucao:
                dias = (self.data_devolucao - self.data_prevista_devolucao).days
                return round(dias * VALOR_DIARIO, 2)
        elif self.esta_atrasado:
            dias = (timezone.now().date() - self.data_prevista_devolucao).days
            return round(dias * VALOR_DIARIO, 2)
        return 0.00

    def __str__(self):
        return f'{self.membro} -> {self.livro}'


class Reserva(models.Model):
    """Modelo para o Desafio Reserva de Livro"""
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)
    atendida = models.BooleanField(default=False)

    def __str__(self):
        return f'Reserva: {self.membro} -> {self.livro}'