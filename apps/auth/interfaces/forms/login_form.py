"""Formulario de inicio de sesión (CU-01)."""

from django import forms

from . import BootstrapFormMixin


class LoginForm(BootstrapFormMixin, forms.Form):
    """Captura usuario y contraseña.

    No valida credenciales: esa responsabilidad vive en `LoginUseCase`
    (separación de responsabilidades). Aquí solo se valida el formato.
    """

    username = forms.CharField(
        label='Usuario',
        max_length=150,
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
    )
