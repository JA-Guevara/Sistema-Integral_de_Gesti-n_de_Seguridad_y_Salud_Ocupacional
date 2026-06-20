"""Vistas del usuario autenticado: perfil y cambio de contraseña.

Ambas exigen sesión activa mediante LoginRequiredMixin (Punto 7).
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.auth.application.use_cases.change_password import ChangePasswordUseCase
from apps.auth.interfaces.forms.password_form import ChangePasswordForm
from apps.auth.interfaces.forms.profile_form import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    """CU-06: visualizar y editar los datos del usuario autenticado."""

    template_name = 'auth/profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil fue actualizado correctamente.')
            return redirect('auth:profile')
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, self.template_name, {'form': form})


class ChangePasswordView(LoginRequiredMixin, View):
    """CU-04: el usuario cambia su contraseña sin perder la sesión."""

    template_name = 'auth/change_password.html'

    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            ChangePasswordUseCase().execute(request, form)
            messages.success(request, 'Tu contraseña fue actualizada correctamente.')
            return redirect('auth:profile')
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, self.template_name, {'form': form})
