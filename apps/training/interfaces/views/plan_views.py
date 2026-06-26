"""Vistas del módulo de capacitaciones."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.training.application.use_cases.asignaciones import (
    AsignarPlan, MarcarCompletado, RegistrarAsistencia, RegistrarAvance,
)
from apps.training.application.use_cases.exceptions import TrainingError
from apps.training.application.use_cases.planes import (
    CancelarPlan, CrearPlan, EditarPlan, ListarPlanes, ObtenerPlan, ResumenCapacitaciones,
)
from apps.training.interfaces.forms.plan_form import PlanForm
from apps.workers.models import Trabajador

VER = "usuarios.ver_capacitaciones"
GESTIONAR = "usuarios.gestionar_capacitaciones"


class PlanListView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request):
        return render(request, "training/lista.html", {
            "planes": ListarPlanes().execute(),
            "resumen": ResumenCapacitaciones().execute(),
        })


class PlanCreateView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def get(self, request):
        return render(request, "training/form.html", {"form": PlanForm(), "plan": None})

    def post(self, request):
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = CrearPlan().execute(form, actor=request.user)
            messages.success(request, "Plan de capacitación creado.")
            return redirect("training:detalle", pk=plan.pk)
        messages.error(request, "Corrige los errores del formulario.")
        return render(request, "training/form.html", {"form": form, "plan": None})


class PlanUpdateView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def get(self, request, pk):
        plan = ObtenerPlan().execute(pk)
        return render(request, "training/form.html", {"form": PlanForm(instance=plan), "plan": plan})

    def post(self, request, pk):
        plan = ObtenerPlan().execute(pk)
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            EditarPlan().execute(form)
            messages.success(request, "Plan actualizado.")
            return redirect("training:detalle", pk=pk)
        return render(request, "training/form.html", {"form": form, "plan": plan})


class PlanDetailView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request, pk):
        plan = ObtenerPlan().execute(pk)
        return render(request, "training/detalle.html", {
            "plan": plan,
            "asignaciones": plan.asignaciones.select_related("trabajador"),
        })


class PlanCancelView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def post(self, request, pk):
        CancelarPlan().execute(pk)
        messages.success(request, "Plan cancelado.")
        return redirect("training:detalle", pk=pk)


class AsignarView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def get(self, request, pk):
        plan = ObtenerPlan().execute(pk)
        asignados = plan.asignaciones.values_list("trabajador_id", flat=True)
        trabajadores = Trabajador.objects.filter(estado=Trabajador.Estado.ACTIVO).exclude(pk__in=asignados)
        return render(request, "training/asignar.html", {"plan": plan, "trabajadores": trabajadores})

    def post(self, request, pk):
        plan = ObtenerPlan().execute(pk)
        try:
            creadas = AsignarPlan().execute(plan, trabajador_ids=request.POST.getlist("trabajadores"), actor=request.user)
            messages.success(request, f"Plan asignado a {creadas} trabajador(es).")
            return redirect("training:detalle", pk=pk)
        except TrainingError as exc:
            messages.error(request, str(exc))
            return redirect("training:asignar", pk=pk)


class AvanceView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def post(self, request, asignacion_id):
        try:
            if request.POST.get("completar") == "1":
                a = MarcarCompletado().execute(asignacion_id)
            else:
                a = RegistrarAvance().execute(asignacion_id, request.POST.get("avance_pct"))
            messages.success(request, "Avance actualizado.")
            return redirect("training:detalle", pk=a.plan_id)
        except TrainingError as exc:
            messages.error(request, str(exc))
            return redirect("training:lista")


class AsistenciaView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def post(self, request, asignacion_id):
        try:
            a = RegistrarAsistencia().execute(
                asignacion_id,
                fecha=request.POST.get("fecha"),
                asistio=request.POST.get("asistio") == "on",
                observacion=request.POST.get("observacion", ""),
            )
            messages.success(request, "Asistencia registrada.")
            return redirect("training:detalle", pk=a.asignacion.plan_id)
        except TrainingError as exc:
            messages.error(request, str(exc))
            return redirect("training:lista")
