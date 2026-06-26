"""Vistas del módulo de reportes (dashboard de cumplimiento + export)."""

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.reports.application.use_cases.cumplimiento import (
    DashboardCumplimiento, ReporteCumplimiento,
)
from apps.reports.application.use_cases.export import exportar_excel, exportar_pdf
from apps.workers.models import Area

VER = "usuarios.ver_reportes"

COLUMNAS = ["Trabajador", "Documento", "Área", "Cargo", "Asignadas", "Rendidas",
            "Aprobadas", "Competencia %", "Brechas", "Capacit.", "Cumple"]


def _fila_export(f):
    t = f["trabajador"]
    return [t.nombre_completo, t.documento, t.area.nombre, t.cargo.nombre,
            f["asignadas"], f["rendidas"], f["aprobadas"], f["competencia"],
            f["brechas"], f["capacitaciones"], "Sí" if f["cumple"] else "No"]


class ReportesDashboardView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request):
        return render(request, "reports/dashboard.html", {
            "resumen": DashboardCumplimiento().execute(),
        })


class ReporteCumplimientoView(PermissionRequiredMixin, View):
    permission_required = VER
    raise_exception = True

    def get(self, request):
        area_id = request.GET.get("area") or None
        filas = ReporteCumplimiento().execute(area_id=area_id)
        export = request.GET.get("export")
        titulo = "Reporte de Cumplimiento SySO — Ley 16998 / ISO 45001"

        if export == "excel":
            return exportar_excel(titulo, COLUMNAS, [_fila_export(f) for f in filas], "cumplimiento.xlsx")
        if export == "pdf":
            return exportar_pdf(titulo, COLUMNAS, [_fila_export(f) for f in filas], "cumplimiento.pdf")

        return render(request, "reports/cumplimiento.html", {
            "filas": filas, "areas": Area.objects.all(), "area_id": area_id,
        })
