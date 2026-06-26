"""Casos de uso de la Evaluacion: CRUD, máquina de estados y estadísticas."""

from django.db.models import Avg, Count, Q

from apps.evaluations.application.use_cases.exceptions import EvaluacionError
from apps.evaluations.models import Evaluacion, Resultado

# Transiciones válidas de la máquina de estados (origen -> destinos permitidos).
TRANSICIONES = {
    Evaluacion.Estado.BORRADOR: {Evaluacion.Estado.PUBLICADA, Evaluacion.Estado.CANCELADA},
    Evaluacion.Estado.PUBLICADA: {Evaluacion.Estado.ABIERTA, Evaluacion.Estado.CANCELADA},
    Evaluacion.Estado.ABIERTA: {Evaluacion.Estado.CERRADA, Evaluacion.Estado.CANCELADA},
    Evaluacion.Estado.CERRADA: {Evaluacion.Estado.ARCHIVADA},
    Evaluacion.Estado.CANCELADA: set(),
    Evaluacion.Estado.ARCHIVADA: set(),
}


class ListarEvaluaciones:
    def execute(self):
        return Evaluacion.objects.select_related("nivel_riesgo").annotate(
            n_preguntas=Count("preguntas", distinct=True),
            n_asignaciones=Count("asignaciones", distinct=True),
        )


class ObtenerEvaluacion:
    def execute(self, evaluacion_id):
        try:
            return Evaluacion.objects.select_related("nivel_riesgo").get(pk=evaluacion_id)
        except Evaluacion.DoesNotExist:
            raise EvaluacionError("La evaluación solicitada no existe.")


class CrearEvaluacion:
    def execute(self, form, actor=None):
        evaluacion = form.save(commit=False)
        evaluacion.creado_por = actor
        evaluacion.save()
        return evaluacion


class EditarEvaluacion:
    def execute(self, evaluacion, form):
        if not evaluacion.editable:
            raise EvaluacionError("Solo se puede editar una evaluación en estado borrador.")
        return form.save()


class CambiarEstadoEvaluacion:
    """Aplica una transición de estado validándola contra la máquina de estados."""

    def execute(self, evaluacion, nuevo_estado):
        permitidos = TRANSICIONES.get(evaluacion.estado, set())
        if nuevo_estado not in permitidos:
            raise EvaluacionError(
                f"No se puede pasar de «{evaluacion.get_estado_display()}» a ese estado."
            )

        # Regla de publicación: debe tener preguntas válidas.
        if nuevo_estado == Evaluacion.Estado.PUBLICADA:
            self._validar_publicable(evaluacion)

        evaluacion.estado = nuevo_estado
        evaluacion.save(update_fields=["estado", "actualizado_en"])
        return evaluacion

    @staticmethod
    def _validar_publicable(evaluacion):
        preguntas = evaluacion.preguntas.prefetch_related("opciones")
        if not preguntas.exists():
            raise EvaluacionError("Agrega al menos una pregunta antes de publicar.")
        for pregunta in preguntas:
            opciones = list(pregunta.opciones.all())
            if len(opciones) < 2:
                raise EvaluacionError(f"La pregunta «{pregunta.enunciado[:40]}…» necesita al menos 2 opciones.")
            if not any(o.es_correcta for o in opciones):
                raise EvaluacionError(f"La pregunta «{pregunta.enunciado[:40]}…» no tiene una opción correcta.")


class GenerarEstadisticas:
    """KPIs de una evaluación: asignados, rendidos, tasa de aprobación, promedio."""

    def execute(self, evaluacion):
        asignaciones = evaluacion.asignaciones.all()
        resultados = Resultado.objects.filter(intento__asignacion__evaluacion=evaluacion)
        total_resultados = resultados.count()
        agg = resultados.aggregate(
            promedio=Avg("porcentaje"),
            aprobados=Count("id", filter=Q(aprobado=True)),
        )
        return {
            "asignados": asignaciones.count(),
            "rendidos": total_resultados,
            "aprobados": agg["aprobados"] or 0,
            "reprobados": total_resultados - (agg["aprobados"] or 0),
            "promedio": round(agg["promedio"] or 0, 1),
            "tasa_aprobacion": round((agg["aprobados"] or 0) / total_resultados * 100, 1) if total_resultados else 0,
        }


class ResumenEvaluaciones:
    """KPIs globales del módulo para las tarjetas del listado."""

    def execute(self):
        qs = Evaluacion.objects.all()
        return {
            "total": qs.count(),
            "abiertas": qs.filter(estado=Evaluacion.Estado.ABIERTA).count(),
            "borradores": qs.filter(estado=Evaluacion.Estado.BORRADOR).count(),
            "rendiciones": Resultado.objects.count(),
        }
