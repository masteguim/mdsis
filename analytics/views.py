from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from goals.models import Goal

User = get_user_model()

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_metas'] = Goal.objects.count()
        context['usuarios_ativos'] = User.objects.filter(is_active=True).count()
        return context