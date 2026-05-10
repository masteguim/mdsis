from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from users.models import UserProfile
from .models import Goal
from .forms import GoalForm


def atualizar_streak(user):
    hoje = timezone.localdate()

    profile, created = UserProfile.objects.get_or_create(user=user)

    if profile.last_activity_date == hoje:
        return

    if profile.last_activity_date == hoje - timezone.timedelta(days=1):
        profile.streak += 1
    else:
        profile.streak = 1

    profile.last_activity_date = hoje
    profile.save()


# DASHBOARD
@login_required
def dashboard_view(request):
    metas = Goal.objects.filter(user=request.user)
    profile, created = UserProfile.objects.get_or_create(user=request.user)

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
        'streak': profile.streak,
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
    concluidas = metas.filter(status='concluida').count()
    pendentes = metas.filter(status='pendente').count()
    andamento = metas.filter(status='andamento').count()

    eficiencia = 0
    andamento_percent = 0
    pendentes_percent = 0

    if total > 0:
        eficiencia = round((concluidas / total) * 100)
        andamento_percent = round((andamento / total) * 100)
        pendentes_percent = round((pendentes / total) * 100)

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


# CONCLUIR META
@login_required
def meta_concluir_view(request, meta_id):
    meta = Goal.objects.get(id=meta_id, user=request.user)
    meta.status = 'concluida'

    if meta.tipo == 'progresso' and meta.quantidade_total:
        meta.quantidade_atual = meta.quantidade_total

    meta.save()

    atualizar_streak(request.user)

    return redirect('metas_list')


# INCREMENTAR META DE PROGRESSO
@login_required
def meta_incrementar_view(request, meta_id):
    meta = Goal.objects.get(id=meta_id, user=request.user)

    if meta.tipo == 'progresso' and meta.quantidade_total:
        if meta.quantidade_atual < meta.quantidade_total:
            meta.quantidade_atual += 1

        if meta.quantidade_atual >= meta.quantidade_total:
            meta.status = 'concluida'

        meta.save()

        atualizar_streak(request.user)

    return redirect('metas_list')


# EXCLUIR META
@login_required
def meta_delete_view(request, meta_id):
    meta = Goal.objects.get(id=meta_id, user=request.user)
    meta.delete()

    return redirect('metas_list')


# EDITAR META
@login_required
def meta_edit_view(request, meta_id):
    meta = Goal.objects.get(id=meta_id, user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=meta)

        if form.is_valid():
            form.save()
            return redirect('metas_list')
    else:
        form = GoalForm(instance=meta)

    return render(request, 'goals/meta_form.html', {
        'form': form,
        'editando': True
    })