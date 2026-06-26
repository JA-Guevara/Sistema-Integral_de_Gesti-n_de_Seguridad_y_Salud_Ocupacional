"""Vistas del módulo de analítica (dashboard, brechas, diagnóstico)."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.analytics.application.use_cases.brechas import ListarBrechas, ValidarBrecha
from apps.analytics.application.use_cases.competencia import CalcularYDetectar, ProcesarTodos
from apps.analytics.application.use_cases.exceptions import AnalyticsError
from apps.analytics.application.use_cases.resumen import DiagnosticoTrabajador, ResumenAnalytics
from apps.analytics.models import Brecha
from apps.workers.application.use_cases.trabajadores import ObtenerTrabajador

VER = "usuarios.ver_analytics"
GESTIONAR = "usuarios.gestionar_analytics"


class DashboardView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request):
        return render(request, "analytics/dashboard.html", {
            "resumen": ResumenAnalytics().execute(),
            "sugeridas": ListarBrechas().execute(estado=Brecha.Estado.SUGERIDA)[:10],
        })


class ProcesarTodosView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def post(self, request):
        res = ProcesarTodos().execute()
        messages.success(
            request,
            f"Análisis ejecutado sobre {res['trabajadores']} trabajador(es): "
            f"{res['brechas_nuevas']} brecha(s) nueva(s) detectada(s).",
        )
        return redirect("analytics:dashboard")


class BrechasListView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request):
        estado = request.GET.get("estado") or None
        return render(request, "analytics/brechas.html", {
            "brechas": ListarBrechas().execute(estado=estado),
            "estado_actual": estado,
        })


class ValidarBrechaView(PermissionRequiredMixin, View):
    permission_required = GESTIONAR
    raise_exception = True

    def post(self, request, brecha_id):
        try:
            ValidarBrecha().execute(brecha_id, request.POST.get("decision"), actor=request.user)
            messages.success(request, "Brecha actualizada.")
        except AnalyticsError as exc:
            messages.error(request, str(exc))
        return redirect("analytics:brechas")


class DiagnosticoView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request, trabajador_id):
        return render(request, "analytics/trabajador.html", DiagnosticoTrabajador().execute(trabajador_id))

    def post(self, request, trabajador_id):
        # Procesar (analizar) este trabajador puntualmente.
        if not request.user.has_perm(GESTIONAR):
            messages.error(request, "No tienes permiso para procesar análisis.")
            return redirect("analytics:diagnostico", trabajador_id=trabajador_id)
        trabajador = ObtenerTrabajador().execute(trabajador_id)
        res = CalcularYDetectar().execute(trabajador)
        messages.success(request, f"Análisis hecho: {res['brechas_nuevas']} brecha(s) nueva(s).")
        return redirect("analytics:diagnostico", trabajador_id=trabajador_id)
