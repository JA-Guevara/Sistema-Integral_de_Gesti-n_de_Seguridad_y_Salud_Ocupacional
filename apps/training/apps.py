from django.apps import AppConfig


class TrainingConfig(AppConfig):
    """Capacitaciones: planes, asignación, avance y asistencia.

    Gestiona los planes; NO imparte formación: el material se referencia por URL.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.training"
    label = "training"
    verbose_name = "Capacitaciones"
