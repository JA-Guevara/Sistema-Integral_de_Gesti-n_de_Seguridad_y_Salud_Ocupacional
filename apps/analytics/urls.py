"""Rutas del módulo de analítica."""

from django.urls import path

from apps.analytics.interfaces.views import analytics_views

app_name = "analytics"

urlpatterns = [
    path("", analytics_views.DashboardView.as_view(), name="dashboard"),
    path("procesar/", analytics_views.ProcesarTodosView.as_view(), name="procesar_todos"),
    path("brechas/", analytics_views.BrechasListView.as_view(), name="brechas"),
    path("brechas/<int:brecha_id>/validar/", analytics_views.ValidarBrechaView.as_view(), name="validar_brecha"),
    path("trabajador/<int:trabajador_id>/", analytics_views.DiagnosticoView.as_view(), name="diagnostico"),
]
