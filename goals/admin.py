from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('quantidade_total', 'quantidade_atual', 'progresso_percentual')

    def progresso_percentual(self, obj):
        if obj.quantidade_total > 0:
            percent = (obj.quantidade_atual / obj.quantidade_total) * 100
            return f"{percent:.2f}%"
        return "0%"

    progresso_percentual.short_description = 'Progresso (%)'