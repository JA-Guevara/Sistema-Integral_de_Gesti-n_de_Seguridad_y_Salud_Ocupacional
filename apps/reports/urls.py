"""Rutas del módulo de reportes."""

from django.urls import path

from apps.reports.interfaces.views import report_views

app_name = "reports"

urlpatterns = [
    path("", report_views.ReportesDashboardView.as_view(), name="dashboard"),
    path("cumplimiento/", report_views.ReporteCumplimientoView.as_view(), name="cumplimiento"),
]
