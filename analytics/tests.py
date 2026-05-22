from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from goals.models import Goal


class AnalyticsAppTestCase(TestCase):

    def setUp(self):
        """Arrange Global para o módulo de Analytics"""
        self.client = Client()

        # Criando Administrador
        self.admin_user = User.objects.create_user(username="adm_painel", password="123", is_staff=True)
        # Criando Usuário Comum
        self.common_user = User.objects.create_user(username="cliente_comum", password="123")

        # Criando uma meta dummy associada ao cliente
        self.meta_dummy = Goal.objects.create(
            user=self.common_user,
            titulo="Meta de Teste Global",
            quantidade_total=10,
            quantidade_atual=2
        )

    def test_admin_dashboard_context_contains_all_goals(self):
        """Garante que o painel ADM lista as metas de todos os utilizadores do sistema."""
        # Arrange
        self.client.login(username="adm_painel", password="123")
        url = reverse("admin_home")

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("metas_globais", response.context)
        self.assertEqual(len(response.context["metas_globais"]), 1)
        self.assertEqual(response.context["metas_globais"][0].titulo, "Meta de Teste Global")

    def test_admin_user_update_view_saves_changes(self):
        """Garante que o ADM consegue alterar o status de um usuário (ex: torná-lo ativo/inativo)."""
        # Arrange
        self.client.login(username="adm_painel", password="123")
        url = reverse("admin_user_edit", kwargs={"pk": self.common_user.pk})
        dados_atualizacao = {
            "username": "cliente_comum",
            "email": "novo_email@teste.com",
            "is_active": False,  # Desativando o usuário
            "is_staff": False
        }

        # Act
        response = self.client.post(url, data=dados_atualizacao)
        self.common_user.refresh_from_db()

        # Assert
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertFalse(self.common_user.is_active)  # O usuário foi desativado no BD
        self.assertEqual(self.common_user.email, "novo_email@teste.com")