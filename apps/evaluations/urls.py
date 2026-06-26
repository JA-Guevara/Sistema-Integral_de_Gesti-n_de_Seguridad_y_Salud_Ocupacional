"""Rutas del módulo de evaluaciones."""

from django.urls import path

from apps.evaluations.interfaces.views import evaluacion_views, resolver_views

app_name = "evaluations"

urlpatterns = [
    path("", evaluacion_views.EvaluacionListView.as_view(), name="lista"),
    path("nueva/", evaluacion_views.EvaluacionCreateView.as_view(), name="crear"),
    path("<int:pk>/", evaluacion_views.EvaluacionDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", evaluacion_views.EvaluacionUpdateView.as_view(), name="editar"),
    path("<int:pk>/estado/", evaluacion_views.EvaluacionEstadoView.as_view(), name="estado"),
    path("<int:pk>/preguntas/", evaluacion_views.PreguntasView.as_view(), name="preguntas"),
    path("<int:pk>/preguntas/<int:pregunta_id>/eliminar/", evaluacion_views.EliminarPreguntaView.as_view(), name="eliminar_pregunta"),
    path("<int:pk>/asignar/", evaluacion_views.AsignarView.as_view(), name="asignar"),
    path("<int:pk>/estadisticas/", evaluacion_views.EstadisticasView.as_view(), name="estadisticas"),

    # Rendición
    path("rendir/<int:asignacion_id>/", resolver_views.ResolverView.as_view(), name="resolver"),
    path("resultado/<int:resultado_id>/", resolver_views.ResultadoView.as_view(), name="resultado"),
]
