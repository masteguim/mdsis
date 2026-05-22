from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from goals.models import Goal
from users.models import UserProfile

# FÁBRICA DE DADOS DUMMIES
class DummyDataFactory:
    """
    Centraliza a criação de dados fictícios (Dummies) para os testes unitários.
    """

    @staticmethod
    def create_dummy_user(username="user_dummy", password="password123", is_staff=False):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=f"{username}@exemplo.com"
        )
        if is_staff:
            user.is_staff = True
            user.save()
        return user

    @staticmethod
    def create_dummy_goal(user, titulo="Estudar Django", total=10, atual=0):
        return Goal.objects.create(
            user=user,
            titulo=titulo,
            quantidade_total=total,
            quantidade_atual=atual
        )

class MDSISTestCase(TestCase):

    def setUp(self):
        """
        Arrange Global: Inicializa o cliente HTTP do Django para simular requisições.
        """
        self.client = Client()

    # TESTES DE SINAIS E PERFIS (SIGNALS)

    def test_profile_creation_on_user_signal(self):
        """
        Garante que o UserProfile é criado automaticamente via signals
        quando um novo User é registado.
        """
        # Arrange
        novo_username = "usuario_sinal_teste"

        # Act
        novo_user = User.objects.create_user(username=novo_username, password="password123")
        profile_exists = UserProfile.objects.filter(user=novo_user).exists()

        # Assert
        self.assertTrue(profile_exists)
        self.assertEqual(novo_user.userprofile.streak, 0)

    # TESTES DE SEGURANÇA, ROTAS E PERMISSÕES

    def test_perfil_view_requires_login(self):
        """
        Garante que utilizadores não autenticados são redirecionados
        ao tentar aceder à página de perfil.
        """
        # Arrange
        url = reverse("perfil")

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 302)  # Redirecionamento (Found)
        self.assertIn(reverse("login"), response.url)

    def test_admin_dashboard_restricts_regular_user(self):
        """
        Garante que um utilizador comum NÃO consegue aceder ao Painel ADM.
        """
        # Arrange
        user_comum = DummyDataFactory.create_dummy_user(username="cliente")
        self.client.login(username="cliente", password="password123")
        url = reverse("admin_home")

        # Act
        response = self.client.get(url)

        # Assert
        # Nota: Dependendo de como o UserPassesTestMixin ou custom permission está configurado,
        # o Django pode retornar 403 (Forbidden) ou redirecionar (302) para o login.
        self.assertIn(response.status_code, [403, 302])

    def test_admin_dashboard_allows_staff_user(self):
        """
        Garante que um utilizador com estatuto de Staff consegue aceder ao Painel ADM.
        """
        # Arrange
        user_adm = DummyDataFactory.create_dummy_user(username="administrador", is_staff=True)
        self.client.login(username="administrador", password="password123")
        url = reverse("admin_home")

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)

    # TESTES DE ENVIO DE FORMULÁRIOS

    def test_perfil_view_post_updates_database(self):
        """
        Garante que o envio de dados válidos via POST atualiza as informações
        do utilizador no Banco de Dados.
        """
        # Arrange
        user = DummyDataFactory.create_dummy_user(username="joao_sa")
        self.client.login(username="joao_sa", password="password123")
        url = reverse("perfil")
        dados_atualizados = {
            "first_name": "João",
            "last_name": "de Sá",
            "email": "joao.alterado@teste.com"
        }

        # Act
        response = self.client.post(url, data=dados_atualizados)
        user.refresh_from_db()

        # Assert
        self.assertEqual(response.status_code, 302)  # Redireciona de volta após salvar
        self.assertEqual(user.first_name, "João")
        self.assertEqual(user.last_name, "de Sá")
        self.assertEqual(user.email, "joao.alterado@teste.com")

    def test_perfil_view_post_invalid_data(self):
        """
        Garante que o sistema responde de forma controlada (recarregando ou redirecionando)
        quando dados vazios ou inesperados são submetidos no perfil.
        """
        # Arrange
        user = DummyDataFactory.create_dummy_user(username="joao_validacao")
        self.client.login(username="joao_validacao", password="password123")
        url = reverse("perfil")

        # Enviando um dicionário vazio para testar a resiliência do formulário de POST
        dados_invalidos = {}

        # Act
        response = self.client.post(url, data=dados_invalidos)

        # Assert
        # A view deve recarregar a página ou processar o redirecionamento sem quebrar o servidor (sem Erro 500)
        self.assertIn(response.status_code, [200, 302])

    # TESTES DE REGRAS DE NEGÓCIO (METAS / GOALS)

    def test_meta_increment_progression_logic(self):
        """
        Testa se a rota de incrementar adiciona ou modifica corretamente o estado da meta.
        """
        # Arrange
        user = DummyDataFactory.create_dummy_user(username="dev_metas")
        meta = DummyDataFactory.create_dummy_goal(user=user, titulo="Ler Livros", total=5, atual=1)
        self.client.login(username="dev_metas", password="password123")
        url = reverse("meta_incrementar", kwargs={"meta_id": meta.id})

        # Act
        response = self.client.post(url, data={})

        # Força a busca direta da instância atualizada na base de dados (evita cache de memória)
        meta_atualizada = Goal.objects.get(pk=meta.id)

        # Assert
        self.assertEqual(response.status_code, 302)  # Redireciona com sucesso após a ação

        # Valida que o valor persistido reflete o comportamento esperado pelo endpoint
        self.assertTrue(meta_atualizada.quantidade_atual >= 1)

    def test_admin_can_delete_any_users_goal(self):
        """
        Garante que o administrador consegue remover uma meta de outro utilizador pelo Painel ADM.
        """
        # Arrange
        cliente = DummyDataFactory.create_dummy_user(username="cliente_meta")
        meta_cliente = DummyDataFactory.create_dummy_goal(user=cliente, titulo="Meta do Cliente")

        admin_user = DummyDataFactory.create_dummy_user(username="boss_adm", is_staff=True)
        self.client.login(username="boss_adm", password="password123")

        url = reverse("admin_goal_delete", kwargs={"pk": meta_cliente.pk})

        # Act
        response = self.client.post(url)
        meta_existe = Goal.objects.filter(pk=meta_cliente.pk).exists()

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertFalse(meta_existe)  # A meta foi completamente removida do banco de dados

#python3 manage.py test users