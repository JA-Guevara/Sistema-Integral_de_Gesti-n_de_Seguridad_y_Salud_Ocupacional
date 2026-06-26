"""Formulario de alta/edición de trabajadores."""

from django import forms
from django.contrib.auth.models import User

from apps.workers.models import Trabajador


class TrabajadorForm(forms.ModelForm):
    """ModelForm sobre Trabajador. La unicidad de `documento` la valida el modelo."""

    class Meta:
        model = Trabajador
        fields = [
            'empresa', 'nombres', 'apellidos', 'documento',
            'cargo', 'area', 'nivel_riesgo', 'supervisor', 'estado',
        ]
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-select'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'nivel_riesgo': forms.Select(attrs={'class': 'form-select'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El supervisor es opcional y se elige entre usuarios activos del sistema.
        self.fields['supervisor'].queryset = User.objects.filter(is_active=True).order_by('first_name', 'username')
        self.fields['supervisor'].required = False
