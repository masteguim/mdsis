from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Goal
from .forms import GoalForm


# DASHBOARD
@login_required
def dashboard_view(request):

    metas = Goal.objects.filter(user=request.user)

    total = metas.count()
    concluidas = metas.filter(status='concluida').count()
    pendentes = metas.filter(status='pendente').count()
    andamento = metas.filter(status='andamento').count()

    eficiencia = 0

    if total > 0:
        eficiencia = round((concluidas / total) * 100)

    context = {
        'total': total,
        'concluidas': concluidas,
        'pendentes': pendentes,
        'andamento': andamento,
        'eficiencia': eficiencia,
    }

    return render(request, 'dashboard/home.html', context)


# LISTA DE METAS
@login_required
def metas_list_view(request):

    metas = Goal.objects.filter(user=request.user)

    return render(request, 'goals/metas_list.html', {
        'metas': metas
    })


# CRIAR META
@login_required
def meta_create_view(request):

    if request.method == 'POST':

        form = GoalForm(request.POST)

        if form.is_valid():

            meta = form.save(commit=False)
            meta.user = request.user
            meta.save()

            return redirect('metas_list')

    else:
        form = GoalForm()

    return render(request, 'goals/meta_form.html', {
        'form': form
    })


# INDICADORES
@login_required
def indicadores_view(request):

    metas = Goal.objects.filter(user=request.user)

    total = metas.count()

    concluidas = metas.filter(
        status='concluida'
    ).count()

    pendentes = metas.filter(
        status='pendente'
    ).count()

    andamento = metas.filter(
        status='andamento'
    ).count()

    eficiencia = 0
    andamento_percent = 0
    pendentes_percent = 0

    if total > 0:

        eficiencia = round(
            (concluidas / total) * 100
        )

        andamento_percent = round(
            (andamento / total) * 100
        )

        pendentes_percent = round(
            (pendentes / total) * 100
        )

    return render(
        request,
        'dashboard/indicadores.html',
        {
            'total': total,
            'concluidas': concluidas,
            'pendentes': pendentes,
            'andamento': andamento,
            'eficiencia': eficiencia,
            'andamento_percent': andamento_percent,
            'pendentes_percent': pendentes_percent,
        }
    )