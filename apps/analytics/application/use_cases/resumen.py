"""Casos de uso de resumen/diagnóstico para el dashboard de analítica."""

from django.db.models import Avg, Count, Q

from apps.analytics.application.use_cases.exceptions import AnalyticsError
from apps.analytics.models import Brecha, NivelCompetencia
from apps.workers.models import Trabajador


class ResumenAnalytics:
    def execute(self):
        brechas = Brecha.objects.all()
        agg = brechas.aggregate(
            sugeridas=Count("id", filter=Q(estado=Brecha.Estado.SUGERIDA)),
            validadas=Count("id", filter=Q(estado=Brecha.Estado.VALIDADA)),
        )
        return {
            "sugeridas": agg["sugeridas"] or 0,
            "validadas": agg["validadas"] or 0,
            "trabajadores_con_brecha": brechas.filter(
                estado__in=[Brecha.Estado.SUGERIDA, Brecha.Estado.VALIDADA]
            ).values("trabajador").distinct().count(),
            "competencia_media": round(
                NivelCompetencia.objects.aggregate(m=Avg("score"))["m"] or 0, 1
            ),
        }


class DiagnosticoTrabajador:
    def execute(self, trabajador_id):
        try:
            trabajador = Trabajador.objects.get(pk=trabajador_id)
        except Trabajador.DoesNotExist:
            raise AnalyticsError("El trabajador solicitado no existe.")
        return {
            "trabajador": trabajador,
            "niveles": trabajador.niveles_competencia.all(),
            "brechas": trabajador.brechas.all(),
        }
