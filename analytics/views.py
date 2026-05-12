from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from django.contrib.auth.models import User
from goals.models import Goal
from django.urls import reverse_lazy
from django.views.generic import DeleteView

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'dashboard/admin_custom.html'
    context_object_name = 'usuarios'

    def test_func(self):
        # Só entra se for membro da equipa (ADM)
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionamos todas as metas de todos os utilizadores ao contexto
        context['metas_globais'] = Goal.objects.all().select_related('user')
        return context

# Exemplo de uma View para editar utilizadores pelo Painel
class AdminUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'is_active', 'is_staff']
    template_name = 'users/admin_user_form.html'
    success_url = reverse_lazy('admin_home')

    def test_func(self):
        return self.request.user.is_staff

class AdminGoalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Goal
    template_name = 'goals/meta_confirm_delete.html' # Aproveita o template de exclusão que você já deve ter
    success_url = reverse_lazy('admin_home')

    def test_func(self):
        return self.request.user.is_staff