from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, UserProfileForm


def cadastro_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    for field in form.fields.values():
        field.widget.attrs.update({"class": "form-control"})

    return render(request, "users/cadastro.html", {"form": form})


@login_required
def perfil_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "users/perfil.html", {"form": form})