from django.apps import AppConfig


class EvaluationsConfig(AppConfig):
    """App del núcleo: evaluaciones de competencias en seguridad ocupacional."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.evaluations"
    label = "evaluations"
    verbose_name = "Evaluaciones"
