"""CU-04: Caso de uso de cambio de contraseña."""

from django.contrib.auth import update_session_auth_hash


class ChangePasswordUseCase:
    """Cambia la contraseña del usuario autenticado manteniendo su sesión."""

    def execute(self, request, form):
        # PasswordChangeForm valida la contraseña actual y guarda la nueva.
        user = form.save()

        # Sin esto, cambiar la contraseña invalida la sesión y desloguea
        # al usuario. update_session_auth_hash mantiene la sesión activa.
        update_session_auth_hash(request, user)
        return user
