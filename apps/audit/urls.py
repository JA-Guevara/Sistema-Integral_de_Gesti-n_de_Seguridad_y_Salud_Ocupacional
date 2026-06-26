"""Rutas del módulo de bitácora."""

from django.urls import path

from apps.audit.interfaces.views import bitacora_views

app_name = "audit"

urlpatterns = [
    path("", bitacora_views.BitacoraListView.as_view(), name="bitacora"),
]
