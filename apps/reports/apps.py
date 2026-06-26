from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """Reportes de cumplimiento (Ley 16998 / ISO 45001) y exportación."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"
    label = "reports"
    verbose_name = "Reportes"
