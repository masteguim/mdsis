from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['titulo', 'descricao', 'status', 'prazo']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light border-0',
                'placeholder': 'Ex: Estudar Cálculo III'
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
        }