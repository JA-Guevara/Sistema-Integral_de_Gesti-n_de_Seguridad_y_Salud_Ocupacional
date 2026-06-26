"""Caso de uso de rendición de una evaluación con calificación automática."""

from django.db import transaction
from django.utils import timezone

from apps.evaluations.application.use_cases.exceptions import EvaluacionError
from apps.evaluations.models import (
    Asignacion, Intento, Opcion, Respuesta, Resultado,
)


class ObtenerAsignacionParaRendir:
    def execute(self, asignacion_id):
        try:
            return Asignacion.objects.select_related(
                "evaluacion", "trabajador"
            ).get(pk=asignacion_id)
        except Asignacion.DoesNotExist:
            raise EvaluacionError("La asignación solicitada no existe.")


class ResolverEvaluacion:
    """Registra el intento, las respuestas y CALIFICA automáticamente.

    `respuestas` = { pregunta_id (int): opcion_id (int) }.
    Calificación ponderada: cada pregunta vale su `ponderacion`; el porcentaje
    es puntaje_obtenido / puntaje_total * 100; aprueba si ≥ umbral.
    """

    @transaction.atomic
    def execute(self, asignacion, respuestas):
        evaluacion = asignacion.evaluacion
        if not evaluacion.admite_rendicion:
            raise EvaluacionError("La evaluación no está abierta para rendición.")
        if asignacion.estado == Asignacion.Estado.COMPLETADA:
            raise EvaluacionError("Esta asignación ya fue rendida (una sola entrega).")

        preguntas = list(evaluacion.preguntas.prefetch_related("opciones"))
        if not preguntas:
            raise EvaluacionError("La evaluación no tiene preguntas.")

        intento = Intento.objects.create(asignacion=asignacion, enviado_en=timezone.now())

        puntaje_total = 0
        puntaje_obtenido = 0
        for pregunta in preguntas:
            puntaje_total += pregunta.ponderacion
            opcion_id = respuestas.get(pregunta.id)
            opcion = None
            es_correcta = False
            if opcion_id:
                opcion = next((o for o in pregunta.opciones.all() if o.id == int(opcion_id)), None)
                es_correcta = bool(opcion and opcion.es_correcta)
            puntaje = pregunta.ponderacion if es_correcta else 0
            puntaje_obtenido += puntaje
            Respuesta.objects.create(
                intento=intento, pregunta=pregunta, opcion=opcion,
                es_correcta=es_correcta, puntaje=puntaje,
            )

        porcentaje = (puntaje_obtenido / puntaje_total * 100) if puntaje_total else 0
        aprobado = porcentaje >= evaluacion.umbral_aprobacion

        resultado = Resultado.objects.create(
            intento=intento,
            puntaje_obtenido=puntaje_obtenido,
            puntaje_total=puntaje_total,
            porcentaje=round(porcentaje, 2),
            aprobado=aprobado,
        )

        asignacion.estado = Asignacion.Estado.COMPLETADA
        asignacion.save(update_fields=["estado"])
        return resultado
