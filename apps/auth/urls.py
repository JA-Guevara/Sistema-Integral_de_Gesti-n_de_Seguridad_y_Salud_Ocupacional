"""Rutas del módulo de autenticación.

El namespace 'auth' permite referenciar las URLs como 'auth:login',
'auth:profile', etc., de forma desacoplada.
"""

from django.urls import path

from apps.auth.interfaces.views import auth_views, profile_views

app_name = 'auth'

urlpatterns = [
    # --- Acceso (públicas) ---
    path('login/', auth_views.LoginView.as_view(), name='login'),                # CU-01
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),             # CU-02
    path('register/', auth_views.RegisterView.as_view(), name='register'),       # CU-03

    # --- Recuperación de contraseña (públicas) --- CU-05
    path('password/forgot/', auth_views.ForgotPasswordView.as_view(), name='forgot_password'),
    path(
        'password/reset/<uidb64>/<token>/',
        auth_views.ResetPasswordConfirmView.as_view(),
        name='password_reset_confirm',
    ),

    # --- Área autenticada (requieren login) ---
    path('profile/', profile_views.ProfileView.as_view(), name='profile'),               # CU-06
    path('profile/password/', profile_views.ChangePasswordView.as_view(), name='change_password'),  # CU-04
]
