"""Vistas de rendición de evaluaciones (rendir + ver resultado)."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.evaluations.application.use_cases.exceptions import EvaluacionError
from apps.evaluations.application.use_cases.resolver import (
    ObtenerAsignacionParaRendir, ResolverEvaluacion,
)
from apps.evaluations.models import Resultado


class ResolverView(PermissionRequiredMixin, View):
    permission_required = "usuarios.ver_evaluaciones"
    raise_exception = True

    def get(self, request, asignacion_id):
        asignacion = ObtenerAsignacionParaRendir().execute(asignacion_id)
        return render(request, "evaluations/resolver.html", {
            "asignacion": asignacion,
            "evaluacion": asignacion.evaluacion,
            "preguntas": asignacion.evaluacion.preguntas.prefetch_related("opciones"),
        })

    def post(self, request, asignacion_id):
        asignacion = ObtenerAsignacionParaRendir().execute(asignacion_id)
        # respuestas: para cada pregunta llega "pregunta_<id>" = opcion_id
        respuestas = {}
        for key, value in request.POST.items():
            if key.startswith("pregunta_") and value:
                try:
                    respuestas[int(key.replace("pregunta_", ""))] = int(value)
                except ValueError:
                    continue
        try:
            resultado = ResolverEvaluacion().execute(asignacion, respuestas)
            messages.success(request, "Evaluación enviada y calificada.")
            return redirect("evaluations:resultado", resultado_id=resultado.pk)
        except EvaluacionError as exc:
            messages.error(request, str(exc))
            return redirect("evaluations:detalle", pk=asignacion.evaluacion_id)


class ResultadoView(PermissionRequiredMixin, View):
    permission_required = "usuarios.ver_evaluaciones"
    raise_exception = True

    def get(self, request, resultado_id):
        try:
            resultado = Resultado.objects.select_related(
                "intento__asignacion__evaluacion", "intento__asignacion__trabajador"
            ).get(pk=resultado_id)
        except Resultado.DoesNotExist:
            messages.error(request, "El resultado solicitado no existe.")
            return redirect("evaluations:lista")
        return render(request, "evaluations/resultado.html", {
            "resultado": resultado,
            "asignacion": resultado.intento.asignacion,
        })
