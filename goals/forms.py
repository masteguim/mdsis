from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal

        fields = [
            'titulo',
            'descricao',
            'status',
            'prazo',
            'tipo',
            'unidade',
            'quantidade_total'
        ]

        widgets = {

            'titulo': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light border-0',
                'placeholder': 'Ex: Ler livro de Física'
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0',
                'rows': 4,
                'placeholder': 'Descreva sua meta...'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select form-select-lg bg-light border-0'
            }),

            'prazo': forms.DateInput(attrs={
                'class': 'form-control form-control-lg bg-light border-0',
                'type': 'date'
            }),

            'tipo': forms.Select(attrs={
                'class': 'form-select form-select-lg bg-light border-0'
            }),

            'unidade': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light border-0',
                'placeholder': 'Ex: capítulos, páginas, aulas'
            }),

            'quantidade_total': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg bg-light border-0',
                'placeholder': 'Ex: 30'
            }),
        }