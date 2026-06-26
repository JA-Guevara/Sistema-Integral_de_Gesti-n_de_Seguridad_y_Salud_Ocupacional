from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Bitácora: registra automáticamente las acciones críticas del sistema."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit"
    label = "audit"
    verbose_name = "Bitácora"

    def ready(self):
        # Conecta los receptores de señales al cargar la app.
        from apps.audit import signals  # noqa: F401
