from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView
from users.views import perfil_view
from goals.views import dashboard_view, metas_list_view, meta_create_view, indicadores_view

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', lambda request: redirect('login')
         ),

    path(
        'dashboard/',dashboard_view,name='home'
    ),

    path(
        'metas/',metas_list_view,name='metas_list'
    ),

    path(
        'metas/nova/',meta_create_view,name='meta_create'
    ),

    path(
        'indicadores/',indicadores_view,name='indicadores'
    ),

    path('perfil/', perfil_view, name='perfil'),

    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),

    path(
        'users/',include('users.urls')
    ),
]
