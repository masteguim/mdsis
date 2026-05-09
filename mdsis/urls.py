from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView
from goals.views import dashboard_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='home'),
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('login')),

    path(
        'dashboard/',
        TemplateView.as_view(template_name='dashboard/home.html'),
        name='home'
    ),
    path('metas/', TemplateView.as_view(template_name='goals/metas_list.html'), name='metas_list'),

    path('indicadores/', TemplateView.as_view(template_name='dashboard/indicadores.html'), name='indicadores'),

    path('perfil/', TemplateView.as_view(template_name='users/perfil.html'), name='perfil'),

    path(
    'metas/nova/',
    TemplateView.as_view(template_name='goals/meta_form.html'),
    name='meta_create'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
]