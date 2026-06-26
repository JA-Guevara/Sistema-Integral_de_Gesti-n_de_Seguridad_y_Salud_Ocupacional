"""Casos de uso de reportes de cumplimiento (agregan datos de otros módulos)."""

from django.db.models import Avg

from apps.analytics.models import Brecha, NivelCompetencia
from apps.evaluations.models import Asignacion, Resultado
from apps.training.models import AsignacionCapacitacion
from apps.workers.models import Trabajador


class ReporteCumplimiento:
    """Una fila por trabajador activo con su estado de cumplimiento normativo."""

    def execute(self, area_id=None):
        trabajadores = (
            Trabajador.objects
            .filter(estado=Trabajador.Estado.ACTIVO)
            .select_related("area", "cargo", "empresa")
        )
        if area_id:
            trabajadores = trabajadores.filter(area_id=area_id)

        filas = []
        for t in trabajadores:
            asignadas = Asignacion.objects.filter(trabajador=t).count()
            rendidas = Resultado.objects.filter(intento__asignacion__trabajador=t).count()
            aprobadas = Resultado.objects.filter(intento__asignacion__trabajador=t, aprobado=True).count()
            competencia = NivelCompetencia.objects.filter(trabajador=t).aggregate(m=Avg("score"))["m"] or 0
            brechas = Brecha.objects.filter(
                trabajador=t, estado__in=[Brecha.Estado.SUGERIDA, Brecha.Estado.VALIDADA]
            ).count()
            cap_total = AsignacionCapacitacion.objects.filter(trabajador=t).count()
            cap_comp = AsignacionCapacitacion.objects.filter(
                trabajador=t, estado=AsignacionCapacitacion.Estado.COMPLETADO
            ).count()
            # Cumple: sin brechas abiertas y con todas sus evaluaciones rendidas.
            cumple = brechas == 0 and (asignadas == 0 or rendidas >= asignadas)
            filas.append({
                "trabajador": t, "asignadas": asignadas, "rendidas": rendidas, "aprobadas": aprobadas,
                "competencia": round(competencia, 1), "brechas": brechas,
                "capacitaciones": f"{cap_comp}/{cap_total}", "cumple": cumple,
            })
        return filas


class DashboardCumplimiento:
    def execute(self):
        filas = ReporteCumplimiento().execute()
        total = len(filas)
        cumplen = sum(1 for f in filas if f["cumple"])
        return {
            "trabajadores": total,
            "cumplen": cumplen,
            "pendientes": total - cumplen,
            "pct_cumplimiento": round(cumplen / total * 100, 1) if total else 0,
            "brechas_abiertas": sum(f["brechas"] for f in filas),
        }
