from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """Analítica: diagnóstico de competencia y detección de brechas.

    La IA SOLO recomienda y diagnostica; NUNCA aprueba aptitud. La validación
    final la hace el Responsable SySO (acción humana auditada).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analytics"
    label = "analytics"
    verbose_name = "Analítica"
