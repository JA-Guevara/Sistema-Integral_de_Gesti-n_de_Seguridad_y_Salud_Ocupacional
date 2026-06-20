from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """App de gestión de Usuarios, Roles y Permisos.

    Consume el sistema nativo de Django (auth.User, auth.Group, auth.Permission)
    pero expone su propia capa (casos de uso, forms, vistas) para tener control
    total de la administración, igual que el módulo `apps.auth`.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
    label = 'usuarios'
    verbose_name = 'Usuarios, roles y permisos'
