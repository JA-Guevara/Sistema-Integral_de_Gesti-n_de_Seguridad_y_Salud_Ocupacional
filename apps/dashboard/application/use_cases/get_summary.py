"""Caso de uso: obtener el resumen (KPIs) para el panel de control.

Hoy solo existe el módulo de autenticación, por lo que únicamente el conteo
de usuarios es un dato real. Los demás KPIs quedan en `None` (se muestran
como "—") y este es el ÚNICO punto que habrá que tocar cuando se creen los
módulos de Trabajadores, Evaluaciones y Capacitaciones.
"""

from django.contrib.auth.models import User


class GetDashboardSummaryUseCase:
    """Reúne los indicadores que se muestran en las tarjetas del dashboard."""

    def execute(self, user):
        from apps.evaluations.models import Evaluacion
        from apps.training.models import PlanCapacitacion
        from apps.workers.models import Trabajador

        return {
            'usuarios': User.objects.count(),
            'trabajadores': Trabajador.objects.count(),
            'evaluaciones': Evaluacion.objects.count(),
            'capacitaciones': PlanCapacitacion.objects.count(),
        }
