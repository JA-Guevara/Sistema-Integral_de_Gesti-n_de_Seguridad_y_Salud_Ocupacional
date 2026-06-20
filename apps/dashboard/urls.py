"""Rutas del panel de control."""

from django.urls import path

from apps.dashboard.interfaces.views import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_views.DashboardView.as_view(), name='index'),
]
