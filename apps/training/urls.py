"""Rutas del módulo de capacitaciones."""

from django.urls import path

from apps.training.interfaces.views import plan_views

app_name = "training"

urlpatterns = [
    path("", plan_views.PlanListView.as_view(), name="lista"),
    path("nuevo/", plan_views.PlanCreateView.as_view(), name="crear"),
    path("<int:pk>/", plan_views.PlanDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", plan_views.PlanUpdateView.as_view(), name="editar"),
    path("<int:pk>/cancelar/", plan_views.PlanCancelView.as_view(), name="cancelar"),
    path("<int:pk>/asignar/", plan_views.AsignarView.as_view(), name="asignar"),
    path("asignacion/<int:asignacion_id>/avance/", plan_views.AvanceView.as_view(), name="avance"),
    path("asignacion/<int:asignacion_id>/asistencia/", plan_views.AsistenciaView.as_view(), name="asistencia"),
]
