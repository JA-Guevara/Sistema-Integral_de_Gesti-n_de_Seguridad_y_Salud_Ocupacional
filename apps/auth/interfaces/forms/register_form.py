"""Formulario de registro de usuarios (CU-03)."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import BootstrapFormMixin


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    """Extiende UserCreationForm para pedir nombres, apellidos y email.

    UserCreationForm ya aporta: username, password1 y password2 (con
    confirmación y validadores de contraseña de Django).
    """

    first_name = forms.CharField(label='Nombres', max_length=150)
    last_name = forms.CharField(label='Apellidos', max_length=150)
    email = forms.EmailField(label='Correo electrónico', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        """Evita correos duplicados (regla de negocio razonable)."""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
        return email

    def save(self, commit=True):
        # super().save cifra la contraseña; aquí completamos los datos extra.
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
