from django.apps import AppConfig


class WorkersConfig(AppConfig):
    """App del padrón de trabajadores y sus catálogos (empresa, área, cargo, riesgo)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.workers'
    label = 'workers'
    verbose_name = 'Trabajadores'
