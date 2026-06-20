from django.apps import AppConfig


class AuthConfig(AppConfig):
    """Configuración de la app de autenticación.

    IMPORTANTE:
    - `name` debe ser la ruta completa del paquete: 'apps.auth'.
    - `label` se redefine a 'app_auth' para EVITAR el choque con la app
      interna `django.contrib.auth`, que ya usa el label 'auth'.
      Sin esto Django lanza: "Application labels aren't unique".
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth'
    label = 'app_auth'
    verbose_name = 'Autenticación'
