"""Rutas del módulo de trabajadores."""

from django.urls import path

from apps.workers.interfaces.views import trabajador_views

app_name = 'workers'

urlpatterns = [
    path('', trabajador_views.TrabajadorListView.as_view(), name='trabajador_list'),
    path('nuevo/', trabajador_views.TrabajadorCreateView.as_view(), name='trabajador_create'),
    path('<int:pk>/', trabajador_views.TrabajadorDetailView.as_view(), name='trabajador_detail'),
    path('<int:pk>/editar/', trabajador_views.TrabajadorUpdateView.as_view(), name='trabajador_update'),
    path('<int:pk>/estado/', trabajador_views.TrabajadorToggleView.as_view(), name='trabajador_toggle'),
]
