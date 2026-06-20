"""Formularios relacionados con contraseñas (CU-04 y CU-05).

Se reutilizan los formularios nativos de Django (que ya incluyen toda la
validación de seguridad) y solo se les aplica el estilo Bootstrap 5.
"""

from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

from . import BootstrapFormMixin


class ChangePasswordForm(BootstrapFormMixin, PasswordChangeForm):
    """CU-04: cambio de contraseña (pide la actual + la nueva y su confirmación)."""


class StyledPasswordResetForm(BootstrapFormMixin, PasswordResetForm):
    """CU-05: solicitud de recuperación (pide el email)."""


class StyledSetPasswordForm(BootstrapFormMixin, SetPasswordForm):
    """CU-05: fijar la nueva contraseña tras validar el token del enlace."""
