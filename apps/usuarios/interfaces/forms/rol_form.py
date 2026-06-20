"""Formulario de alta/edición de roles.

Solo cubre los datos simples del rol (nombre, descripción, estado). Los
permisos se renderizan agrupados por módulo en la plantilla y se leen de
`request.POST` en la vista, porque requieren un layout personalizado.
"""

from django import forms


class RolForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        max_length=80,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Responsable SySO'}),
    )
    description = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                     'placeholder': 'Alcance y responsabilidad del rol'}),
    )
    active = forms.BooleanField(
        label='Activo',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
