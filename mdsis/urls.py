from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from analytics.views import AdminDashboardView, AdminUserUpdateView, AdminGoalDeleteView
from users.views import perfil_view

from goals.views import dashboard_view, metas_list_view, meta_create_view, indicadores_view, meta_edit_view, meta_concluir_view, meta_incrementar_view, meta_delete_view

urlpatterns = [
    path('', lambda request: redirect('login')),

    path('painel/', AdminDashboardView.as_view(), name='admin_home'),
    path('painel/usuario/<int:pk>/editar/', AdminUserUpdateView.as_view(), name='admin_user_edit'),
    path('painel/meta/<int:pk>/excluir/', AdminGoalDeleteView.as_view(), name='admin_goal_delete'),

    path('admin/', admin.site.urls),

    path('dashboard/', dashboard_view, name='home'),
    path('metas/', metas_list_view, name='metas_list'),
    path('metas/nova/', meta_create_view, name='meta_create'),
    path('indicadores/', indicadores_view, name='indicadores'),
    path('perfil/', perfil_view, name='perfil'),

    path('metas/<int:meta_id>/editar/', meta_edit_view, name='meta_edit'),
    path('metas/<int:meta_id>/concluir/', meta_concluir_view, name='meta_concluir'),
    path('metas/<int:meta_id>/incrementar/', meta_incrementar_view, name='meta_incrementar'),
    path('metas/<int:meta_id>/excluir/', meta_delete_view, name='meta_delete'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
]