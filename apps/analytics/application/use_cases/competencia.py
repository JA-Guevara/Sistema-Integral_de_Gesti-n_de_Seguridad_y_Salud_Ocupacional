"""Casos de uso: cálculo de nivel de competencia y detección de brechas."""

from django.db.models import Avg

from apps.analytics.application.provider_factory import get_analytics_provider
from apps.analytics.models import Brecha, NivelCompetencia
from apps.evaluations.models import Resultado
from apps.workers.models import Trabajador


class CalcularYDetectar:
    """Calcula la competencia por área de un trabajador (a partir de sus
    resultados) y detecta brechas usando el `IAnalyticsProvider` inyectado.

    Las brechas nacen como `sugerida`; NO se aprueba ni rechaza aptitud aquí.
    """

    def __init__(self, provider=None):
        self.provider = provider or get_analytics_provider()

    def execute(self, trabajador):
        # 1) Competencia promedio por área temática (desde Resultado).
        filas = (
            Resultado.objects
            .filter(intento__asignacion__trabajador=trabajador)
            .values("intento__asignacion__evaluacion__area_tema")
            .annotate(score=Avg("porcentaje"))
        )
        niveles = [
            {"area_tema": f["intento__asignacion__evaluacion__area_tema"], "score": f["score"] or 0}
            for f in filas if f["intento__asignacion__evaluacion__area_tema"]
        ]

        # 2) Persistir el nivel de competencia por área.
        for n in niveles:
            NivelCompetencia.objects.update_or_create(
                trabajador=trabajador, area_tema=n["area_tema"],
                defaults={"score": round(n["score"], 2)},
            )

        # 3) Detectar brechas (vía proveedor) evitando duplicar las abiertas.
        detectadas = self.provider.detectar_brechas(niveles)
        nuevas = 0
        for d in detectadas:
            existe = Brecha.objects.filter(
                trabajador=trabajador, area_tema=d["area_tema"],
                estado__in=[Brecha.Estado.SUGERIDA, Brecha.Estado.VALIDADA],
            ).exists()
            if existe:
                continue
            Brecha.objects.create(
                trabajador=trabajador, area_tema=d["area_tema"],
                nivel_detectado=d["nivel_detectado"], descripcion=d["descripcion"],
            )
            nuevas += 1
        return {"areas": len(niveles), "brechas_nuevas": nuevas}


class ProcesarTodos:
    """Ejecuta el análisis para todos los trabajadores activos."""

    def execute(self):
        uc = CalcularYDetectar()
        trabajadores = Trabajador.objects.filter(estado=Trabajador.Estado.ACTIVO)
        total_brechas = 0
        for trabajador in trabajadores:
            total_brechas += uc.execute(trabajador)["brechas_nuevas"]
        return {"trabajadores": trabajadores.count(), "brechas_nuevas": total_brechas}
