from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('login')),

    path(
        'dashboard/',
        TemplateView.as_view(template_name='dashboard/home.html'),
        name='home'
    ),

    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
]