from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Autor, Livro, Emprestimo

class BibliotecaTestCase(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nome="Machado de Assis")
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            isbn="9788535902777",
            data_publicacao="1899-01-01",
            quantidade_exemplares=2,
            autor=self.autor
        )
        self.leitor = User.objects.create_user(username="leitor_teste", password="123")

    def test_disponibilidade_livro(self):
        self.assertTrue(self.livro.disponivel)
        self.livro.quantidade_exemplares = 0
        self.livro.save()
        self.assertFalse(self.livro.disponivel)

    def test_calculo_multa_atraso(self):
        # Cria empréstimo com data de devolução há 3 dias no passado
        data_prevista = timezone.now().date() - timedelta(days=3)
        emprestimo = Emprestimo.objects.create(
            leitor=self.leitor,
            livro=self.livro,
            data_devolucao_prevista=data_prevista,
            status='A'
        )
        # Multa esperada: 3 dias * R$ 2.00 = R$ 6.00
        self.assertEqual(emprestimo.valor_multa, 6.00)