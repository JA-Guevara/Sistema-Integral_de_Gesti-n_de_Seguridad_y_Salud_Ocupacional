"""Formulario de edición del perfil (CU-06).

NOTA DE ARQUITECTURA: este archivo se añade a la estructura original porque
el CU-06 (editar nombre, apellido y email) necesita su propio formulario y
no encaja conceptualmente con los formularios de contraseña.
"""

from django import forms
from django.contrib.auth.models import User

from . import BootstrapFormMixin


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    """Permite al usuario autenticado editar sus datos básicos."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
        }

    def clean_email(self):
        """El email debe ser único, excluyendo al propio usuario."""
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if email and qs.exists():
            raise forms.ValidationError('Ya existe otra cuenta con este correo electrónico.')
        return email
