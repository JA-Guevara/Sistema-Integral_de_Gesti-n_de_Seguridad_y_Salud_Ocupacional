"""Rutas del módulo de Usuarios, Roles y Permisos."""

from django.urls import path

from apps.usuarios.interfaces.views import rol_views, usuario_views

app_name = 'usuarios'

urlpatterns = [
    # --- Roles ---
    path('roles/', rol_views.RolListView.as_view(), name='rol_list'),
    path('roles/nuevo/', rol_views.RolCreateView.as_view(), name='rol_create'),
    path('roles/<int:pk>/', rol_views.RolDetailView.as_view(), name='rol_detail'),
    path('roles/<int:pk>/editar/', rol_views.RolUpdateView.as_view(), name='rol_update'),
    path('roles/<int:pk>/estado/', rol_views.RolToggleView.as_view(), name='rol_toggle'),

    # --- Asignación masiva de rol ---
    path('asignar-rol/', usuario_views.UsuarioBulkRoleView.as_view(), name='user_bulk_role'),

    # --- Usuarios ---
    path('', usuario_views.UsuarioListView.as_view(), name='user_list'),
    path('nuevo/', usuario_views.UsuarioCreateView.as_view(), name='user_create'),
    path('<int:pk>/', usuario_views.UsuarioDetailView.as_view(), name='user_detail'),
    path('<int:pk>/editar/', usuario_views.UsuarioUpdateView.as_view(), name='user_update'),
    path('<int:pk>/estado/', usuario_views.UsuarioToggleView.as_view(), name='user_toggle'),
    path('<int:pk>/reset-password/', usuario_views.UsuarioResetPasswordView.as_view(), name='user_reset_password'),
]
