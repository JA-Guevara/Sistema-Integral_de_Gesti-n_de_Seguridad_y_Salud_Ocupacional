"""Vistas de gestión de evaluaciones (crear, preguntas, estados, asignar)."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.evaluations.application.use_cases.asignaciones import (
    AsignarEvaluacion, AutoAsignarPorRiesgo,
)
from apps.evaluations.application.use_cases.evaluaciones import (
    CambiarEstadoEvaluacion, CrearEvaluacion, EditarEvaluacion, GenerarEstadisticas,
    ListarEvaluaciones, ObtenerEvaluacion, ResumenEvaluaciones,
)
from apps.evaluations.application.use_cases.exceptions import EvaluacionError
from apps.evaluations.application.use_cases.preguntas import AgregarPregunta, EliminarPregunta
from apps.evaluations.interfaces.forms.evaluacion_form import EvaluacionForm
from apps.evaluations.models import Evaluacion
from apps.workers.models import Trabajador

VER = "usuarios.ver_evaluaciones"
GESTIONAR = "usuarios.gestionar_evaluaciones"


class EvaluacionListView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request):
        return render(request, "evaluations/lista.html", {
            "evaluaciones": ListarEvaluaciones().execute(),
            "resumen": ResumenEvaluaciones().execute(),
        })


class EvaluacionCreateView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def get(self, request):
        return render(request, "evaluations/form.html", {"form": EvaluacionForm(), "evaluacion": None})

    def post(self, request):
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = CrearEvaluacion().execute(form, actor=request.user)
            messages.success(request, "Evaluación creada. Ahora agrega sus preguntas.")
            return redirect("evaluations:preguntas", pk=evaluacion.pk)
        messages.error(request, "Corrige los errores del formulario.")
        return render(request, "evaluations/form.html", {"form": form, "evaluacion": None})


class EvaluacionUpdateView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def get(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        return render(request, "evaluations/form.html", {
            "form": EvaluacionForm(instance=evaluacion), "evaluacion": evaluacion,
        })

    def post(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
            try:
                EditarEvaluacion().execute(evaluacion, form)
                messages.success(request, "Evaluación actualizada.")
                return redirect("evaluations:detalle", pk=pk)
            except EvaluacionError as exc:
                messages.error(request, str(exc))
        return render(request, "evaluations/form.html", {"form": form, "evaluacion": evaluacion})


class EvaluacionDetailView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        return render(request, "evaluations/detalle.html", {
            "evaluacion": evaluacion,
            "preguntas": evaluacion.preguntas.prefetch_related("opciones"),
            "asignaciones": evaluacion.asignaciones.select_related("trabajador"),
        })


class EvaluacionEstadoView(PermissionRequiredMixin, View):
    """Aplica una transición de estado (publicar/abrir/cerrar/cancelar/archivar)."""

    permission_required = GESTIONAR
    raise_exception = True

    def post(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        nuevo_estado = request.POST.get("estado")
        try:
            CambiarEstadoEvaluacion().execute(evaluacion, nuevo_estado)
            messages.success(request, f"Evaluación marcada como «{evaluacion.get_estado_display()}».")
        except EvaluacionError as exc:
            messages.error(request, str(exc))
        return redirect("evaluations:detalle", pk=pk)


class PreguntasView(PermissionRequiredMixin, View):
    """Constructor de preguntas (listar + agregar). Solo en borrador."""

    permission_required = GESTIONAR
    raise_exception = True

    def get(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        return render(request, "evaluations/preguntas.html", {
            "evaluacion": evaluacion,
            "preguntas": evaluacion.preguntas.prefetch_related("opciones"),
        })

    def post(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        # Las opciones llegan como listas paralelas: opcion_texto[] + correcta=índice(s)
        textos = request.POST.getlist("opcion_texto")
        correctas = request.POST.getlist("correcta")  # valores = índice de la opción
        opciones = [
            {"texto": t, "es_correcta": str(i) in correctas}
            for i, t in enumerate(textos)
        ]
        try:
            AgregarPregunta().execute(
                evaluacion,
                enunciado=request.POST.get("enunciado"),
                tipo=request.POST.get("tipo", "opcion_multiple"),
                ponderacion=request.POST.get("ponderacion", 1),
                opciones=opciones,
            )
            messages.success(request, "Pregunta agregada.")
        except EvaluacionError as exc:
            messages.error(request, str(exc))
        return redirect("evaluations:preguntas", pk=pk)


class EliminarPreguntaView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def post(self, request, pk, pregunta_id):
        evaluacion = ObtenerEvaluacion().execute(pk)
        try:
            EliminarPregunta().execute(evaluacion, pregunta_id)
            messages.success(request, "Pregunta eliminada.")
        except EvaluacionError as exc:
            messages.error(request, str(exc))
        return redirect("evaluations:preguntas", pk=pk)


class AsignarView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def get(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        asignados = evaluacion.asignaciones.values_list("trabajador_id", flat=True)
        trabajadores = Trabajador.objects.filter(estado=Trabajador.Estado.ACTIVO).exclude(pk__in=asignados)
        return render(request, "evaluations/asignar.html", {
            "evaluacion": evaluacion, "trabajadores": trabajadores,
        })

    def post(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        try:
            if request.POST.get("auto") == "1":
                creadas = AutoAsignarPorRiesgo().execute(evaluacion, actor=request.user)
            else:
                creadas = AsignarEvaluacion().execute(
                    evaluacion,
                    trabajador_ids=request.POST.getlist("trabajadores"),
                    actor=request.user,
                )
            messages.success(request, f"Evaluación asignada a {creadas} trabajador(es).")
            return redirect("evaluations:detalle", pk=pk)
        except EvaluacionError as exc:
            messages.error(request, str(exc))
        return redirect("evaluations:asignar", pk=pk)


class EstadisticasView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request, pk):
        evaluacion = ObtenerEvaluacion().execute(pk)
        return render(request, "evaluations/estadisticas.html", {
            "evaluacion": evaluacion,
            "stats": GenerarEstadisticas().execute(evaluacion),
        })
