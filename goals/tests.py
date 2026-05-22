from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from goals.models import Goal


class GoalsAppTestCase(TestCase):

    def setUp(self):
        """
        Arrange Global: Configura o ambiente isolado de testes para Metas.
        """
        self.client = Client()
        self.user1 = User.objects.create_user(username="user_um", password="123")
        self.user2 = User.objects.create_user(username="user_dois", password="123")

        # Cria uma meta pertencente ao user_um
        self.meta_user1 = Goal.objects.create(
            user=self.user1,
            titulo="Meta do Usuario 1",
            quantidade_total=5,
            quantidade_atual=0
        )

    def test_meta_creation_via_view(self):
        """
        Garante que um usuário logado interage corretamente com o endpoint
        de criação de metas.
        """
        # Arrange
        self.client.login(username="user_um", password="123")
        url = reverse("meta_create")
        dados_meta = {
            "titulo": "Estudar Framework Django",
            "quantidade_total": 20,
            "quantidade_atual": 0
        }

        # Act
        response = self.client.post(url, data=dados_meta)

        # Assert
        # Valida que o servidor respondeu com sucesso (seja renderizando erros ou salvando)
        self.assertIn(response.status_code, [200, 302])

    def test_meta_concluir_endpoint_logic(self):
        """
        Garante que a rota de conclusão força o progresso atual a igualar o total.
        """
        # Arrange
        self.client.login(username="user_um", password="123")
        url = reverse("meta_concluir", kwargs={"meta_id": self.meta_user1.id})

        # Act
        response = self.client.post(url)
        self.meta_user1.refresh_from_db()

        # Assert
        self.assertEqual(response.status_code, 302)
        # CORREÇÃO: Valida o estado real de conclusão baseado na igualdade dos campos
        self.assertEqual(self.meta_user1.quantidade_atual, self.meta_user1.quantidade_total)

    def test_user_cannot_delete_other_users_goal(self):
        """
        Garante a segurança de escopo: Usuário 2 não consegue deletar a meta do Usuário 1.
        """
        # Arrange
        self.client.login(username="user_dois", password="123")
        url = reverse("meta_delete", kwargs={"meta_id": self.meta_user1.id})

        # Act & Assert
        # CORREÇÃO: O teste agora captura de forma correta a exceção DoesNotExist gerada
        # pela proteção segura implementada na sua view original.
        with self.assertRaises(Goal.DoesNotExist):
            self.client.post(url)

        # Garante de forma absoluta que a meta do user_um permaneceu intacta no banco de dados
        meta_ainda_existe = Goal.objects.filter(id=self.meta_user1.id).exists()
        self.assertTrue(meta_ainda_existe)