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
        return {
            # Dato real disponible hoy:
            'usuarios': User.objects.count(),

            # Pendientes hasta que existan sus módulos:
            'trabajadores': None,      # from apps.trabajadores.models import Trabajador
            'evaluaciones': None,      # from apps.evaluaciones.models import Evaluacion
            'capacitaciones': None,    # from apps.capacitaciones.models import Capacitacion
        }
