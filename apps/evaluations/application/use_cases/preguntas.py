"""Casos de uso para gestionar las preguntas y opciones de una evaluación."""

from django.db import transaction

from apps.evaluations.application.use_cases.exceptions import EvaluacionError
from apps.evaluations.models import Opcion, Pregunta


class AgregarPregunta:
    """Crea una pregunta con sus opciones. Solo en estado borrador."""

    @transaction.atomic
    def execute(self, evaluacion, *, enunciado, tipo, ponderacion, opciones):
        if not evaluacion.editable:
            raise EvaluacionError("Solo se pueden gestionar preguntas en estado borrador.")

        enunciado = (enunciado or "").strip()
        if not enunciado:
            raise EvaluacionError("El enunciado es obligatorio.")

        # opciones = [{'texto': str, 'es_correcta': bool}, ...]
        validas = [o for o in opciones if (o.get("texto") or "").strip()]
        if len(validas) < 2:
            raise EvaluacionError("Agrega al menos 2 opciones.")
        if not any(o["es_correcta"] for o in validas):
            raise EvaluacionError("Marca al menos una opción como correcta.")

        siguiente_orden = evaluacion.preguntas.count() + 1
        pregunta = Pregunta.objects.create(
            evaluacion=evaluacion,
            enunciado=enunciado,
            tipo=tipo,
            ponderacion=max(1, int(ponderacion or 1)),
            orden=siguiente_orden,
        )
        for i, o in enumerate(validas, start=1):
            Opcion.objects.create(
                pregunta=pregunta, texto=o["texto"].strip(),
                es_correcta=bool(o["es_correcta"]), orden=i,
            )
        return pregunta


class EliminarPregunta:
    def execute(self, evaluacion, pregunta_id):
        if not evaluacion.editable:
            raise EvaluacionError("Solo se pueden eliminar preguntas en estado borrador.")
        Pregunta.objects.filter(pk=pregunta_id, evaluacion=evaluacion).delete()
