"""CU-01: Caso de uso de inicio de sesión."""

from django.contrib.auth import authenticate, login

from .exceptions import AuthError


class LoginUseCase:
    """Valida credenciales, verifica que el usuario esté activo e inicia sesión.

    Concentra la lógica de negocio del login (Single Responsibility):
    la vista solo se ocupa de HTTP, este caso de uso de las reglas.
    """

    def execute(self, request, username, password):
        # 1) Validar credenciales con el backend de Django.
        #    Con el ModelBackend por defecto, un usuario inactivo devuelve None.
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise AuthError('Usuario o contraseña incorrectos.')

        # 2) Verificación explícita de usuario activo (defensa en profundidad).
        if not user.is_active:
            raise AuthError('Tu cuenta está inactiva. Contacta al administrador.')

        # 3) Crear la sesión (autenticación basada en sesiones).
        login(request, user)
        return user
