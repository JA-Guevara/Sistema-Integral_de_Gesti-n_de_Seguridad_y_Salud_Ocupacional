"""CU-02: Caso de uso de cierre de sesión."""

from django.contrib.auth import logout


class LogoutUseCase:
    """Cierra la sesión del usuario actual y destruye los datos de sesión."""

    def execute(self, request):
        # logout() limpia la sesión y elimina la cookie de sesión del usuario.
        logout(request)
