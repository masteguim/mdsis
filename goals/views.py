from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Goal

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
# Create your views here.
