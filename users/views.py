from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login


def cadastro_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    for field in form.fields.values():
        field.widget.attrs.update({"class": "form-control"})

    return render(request, "users/cadastro.html", {"form": form})