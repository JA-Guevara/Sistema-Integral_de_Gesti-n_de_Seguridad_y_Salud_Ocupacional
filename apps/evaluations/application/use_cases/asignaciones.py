"""Casos de uso de asignación de evaluaciones a trabajadores."""

from apps.evaluations.application.use_cases.exceptions import EvaluacionError
from apps.evaluations.models import Asignacion, Evaluacion
from apps.workers.models import Trabajador


def _validar_asignable(evaluacion):
    if evaluacion.estado not in (Evaluacion.Estado.PUBLICADA, Evaluacion.Estado.ABIERTA):
        raise EvaluacionError("Solo se puede asignar una evaluación publicada o abierta.")


class AsignarEvaluacion:
    """Asigna manualmente una evaluación a una lista de trabajadores (sin duplicar)."""

    def execute(self, evaluacion, *, trabajador_ids, actor=None):
        _validar_asignable(evaluacion)
        trabajadores = Trabajador.objects.filter(pk__in=trabajador_ids, estado=Trabajador.Estado.ACTIVO)
        if not trabajadores.exists():
            raise EvaluacionError("Selecciona al menos un trabajador activo.")

        creadas = 0
        for trabajador in trabajadores:
            _, creada = Asignacion.objects.get_or_create(
                evaluacion=evaluacion, trabajador=trabajador,
                defaults={"asignado_por": actor, "origen": Asignacion.Origen.MANUAL},
            )
            creadas += int(creada)
        return creadas


class AutoAsignarPorRiesgo:
    """Asigna la evaluación a todos los trabajadores activos cuyo nivel de riesgo
    coincide con el nivel objetivo de la evaluación (origen = automática)."""

    def execute(self, evaluacion, *, actor=None):
        _validar_asignable(evaluacion)
        if evaluacion.nivel_riesgo_id is None:
            raise EvaluacionError("La evaluación no tiene un nivel de riesgo objetivo definido.")

        trabajadores = Trabajador.objects.filter(
            estado=Trabajador.Estado.ACTIVO, nivel_riesgo_id=evaluacion.nivel_riesgo_id,
        )
        creadas = 0
        for trabajador in trabajadores:
            _, creada = Asignacion.objects.get_or_create(
                evaluacion=evaluacion, trabajador=trabajador,
                defaults={"asignado_por": actor, "origen": Asignacion.Origen.AUTO_RIESGO},
            )
            creadas += int(creada)
        return creadas
