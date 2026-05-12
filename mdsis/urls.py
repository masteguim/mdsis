from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView

# IMPORT CORRIGIDO: apontando para o app onde a view foi criada
from analytics.views import AdminDashboardView

from goals.views import (
    dashboard_view,
    metas_list_view,
    meta_create_view,
    indicadores_view,
    meta_edit_view,
    meta_concluir_view,
    meta_incrementar_view,
    meta_delete_view,
)

urlpatterns = [
    # Rota raiz redireciona para o login
    path('', lambda request: redirect('login')),

    # Caminho específico para o seu Admin Customizado
    path('painel/', AdminDashboardView.as_view(), name='admin_home'),

    # Admin padrão do Django
    path('admin/', admin.site.urls),

    # Demais rotas
    path('dashboard/', dashboard_view, name='home'),
    path('metas/', metas_list_view, name='metas_list'),
    path('metas/nova/', meta_create_view, name='meta_create'),
    path('indicadores/', indicadores_view, name='indicadores'),

    path('perfil/', TemplateView.as_view(template_name='users/perfil.html'), name='perfil'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),

    path('metas/<int:meta_id>/editar/', meta_edit_view, name='meta_edit'),
    path('metas/<int:meta_id>/concluir/', meta_concluir_view, name='meta_concluir'),
    path('metas/<int:meta_id>/incrementar/', meta_incrementar_view, name='meta_incrementar'),
    path('metas/<int:meta_id>/excluir/', meta_delete_view, name='meta_delete'),
]