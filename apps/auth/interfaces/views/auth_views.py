"""Vistas de autenticación: login, logout, registro y recuperación.

Las vistas son delgadas: traducen HTTP <-> casos de uso y gestionan los
mensajes (Django Messages). La lógica de negocio vive en los use cases.
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from apps.auth.application.use_cases.exceptions import AuthError
from apps.auth.application.use_cases.login import LoginUseCase
from apps.auth.application.use_cases.logout import LogoutUseCase
from apps.auth.application.use_cases.register import RegisterUseCase
from apps.auth.application.use_cases.reset_password import ResetPasswordUseCase
from apps.auth.interfaces.forms.login_form import LoginForm
from apps.auth.interfaces.forms.password_form import (
    StyledPasswordResetForm,
    StyledSetPasswordForm,
)
from apps.auth.interfaces.forms.register_form import RegisterForm


class LoginView(View):
    """CU-01: inicio de sesión basado en sesiones."""

    template_name = 'auth/login.html'

    def get(self, request):
        # Si ya está autenticado, lo mandamos directo al destino post-login.
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = LoginUseCase().execute(
                    request,
                    form.cleaned_data['username'],
                    form.cleaned_data['password'],
                )
                messages.success(request, f'¡Bienvenido, {user.get_short_name() or user.username}!')
                return redirect(self._safe_redirect(request))
            except AuthError as exc:
                messages.error(request, str(exc))
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def _safe_redirect(request):
        """Punto 8: redirección automática respetando ?next= de forma segura.

        Valida el destino para evitar 'open redirects' a sitios externos.
        """
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return next_url
        return settings.LOGIN_REDIRECT_URL


class LogoutView(LoginRequiredMixin, View):
    """CU-02: cierre de sesión. Solo por POST (buena práctica de seguridad)."""

    def post(self, request):
        LogoutUseCase().execute(request)
        messages.info(request, 'Has cerrado sesión correctamente.')
        return redirect('auth:login')


class RegisterView(View):
    """CU-03: registro de nuevos usuarios."""

    template_name = 'auth/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            RegisterUseCase().execute(form)
            messages.success(request, 'Cuenta creada con éxito. Ya puedes iniciar sesión.')
            return redirect('auth:login')
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, self.template_name, {'form': form})


class ForgotPasswordView(View):
    """CU-05 (solicitud): el usuario ingresa su email y se le envía el enlace."""

    template_name = 'auth/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': StyledPasswordResetForm()})

    def post(self, request):
        form = StyledPasswordResetForm(request.POST)
        if form.is_valid():
            ResetPasswordUseCase().send_reset_email(request, form)
            # Mensaje neutro: no revela si el email existe (anti-enumeración).
            messages.success(
                request,
                'Si el correo está registrado, te enviamos un enlace para restablecer tu contraseña.',
            )
            return redirect('auth:login')
        return render(request, self.template_name, {'form': form})


class ResetPasswordConfirmView(PasswordResetConfirmView):
    """CU-05 (confirmación): valida el token del enlace y fija la nueva contraseña.

    Se hereda de la vista nativa de Django porque ya valida el token de forma
    segura. Solo personalizamos plantilla, formulario, destino y el mensaje.
    """

    template_name = 'auth/reset_password.html'
    form_class = StyledSetPasswordForm
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        messages.success(self.request, 'Tu contraseña fue restablecida. Ya puedes iniciar sesión.')
        return super().form_valid(form)
