"""Vistas de administración de USUARIOS."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.usuarios.application.use_cases.exceptions import UsuarioError
from apps.usuarios.application.use_cases.roles import ListarRoles
from apps.usuarios.application.use_cases.usuarios import (
    ActualizarUsuario,
    AsignarRolMasivo,
    CambiarEstadoUsuario,
    CrearUsuario,
    ListarUsuarios,
    ObtenerUsuario,
    ResetearPasswordUsuario,
)
from apps.usuarios.interfaces.forms.usuario_form import UsuarioForm


class UsuarioListView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.ver_usuarios'
    raise_exception = True

    def get(self, request):
        return render(request, 'usuarios/usuarios/lista.html', {
            'usuarios': ListarUsuarios().execute(),
            'roles': ListarRoles().execute(),
        })


class UsuarioCreateView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_usuarios'
    raise_exception = True

    def get(self, request):
        return render(request, 'usuarios/usuarios/form.html', {
            'form': UsuarioForm(require_password=True, initial={'is_active': True}),
            'usuario': None,
        })

    def post(self, request):
        form = UsuarioForm(request.POST, require_password=True)
        if form.is_valid():
            usuario = CrearUsuario().execute(form)
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuarios:user_detail', pk=usuario.pk)
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, 'usuarios/usuarios/form.html', {'form': form, 'usuario': None})


class UsuarioUpdateView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_usuarios'
    raise_exception = True

    def get(self, request, pk):
        usuario = ObtenerUsuario().execute(pk)
        return render(request, 'usuarios/usuarios/form.html', {
            'form': UsuarioForm(instance=usuario),
            'usuario': usuario,
        })

    def post(self, request, pk):
        usuario = ObtenerUsuario().execute(pk)
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            ActualizarUsuario().execute(form)
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios:user_detail', pk=pk)
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, 'usuarios/usuarios/form.html', {'form': form, 'usuario': usuario})


class UsuarioDetailView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.ver_usuarios'
    raise_exception = True

    def get(self, request, pk):
        usuario = ObtenerUsuario().execute(pk)
        return render(request, 'usuarios/usuarios/detalle.html', {
            'usuario': usuario,
            'roles': usuario.groups.order_by('name'),
        })


class UsuarioToggleView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_usuarios'
    raise_exception = True

    def post(self, request, pk):
        try:
            CambiarEstadoUsuario().execute(pk, actor_id=request.user.pk)
            messages.success(request, 'Estado del usuario actualizado correctamente.')
        except UsuarioError as exc:
            messages.error(request, str(exc))
        return redirect('usuarios:user_list')


class UsuarioResetPasswordView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_usuarios'
    raise_exception = True

    def post(self, request, pk):
        try:
            ResetearPasswordUsuario().execute(request, pk)
            messages.success(request, 'Enlace de recuperación enviado al correo del usuario.')
        except UsuarioError as exc:
            messages.error(request, str(exc))
        return redirect('usuarios:user_detail', pk=pk)


class UsuarioBulkRoleView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_usuarios'
    raise_exception = True

    def post(self, request):
        try:
            actualizados = AsignarRolMasivo().execute(
                rol_id=request.POST.get('roleId') or 0,
                user_ids=request.POST.getlist('usuarios'),
            )
            messages.success(request, f'Rol asignado a {actualizados} usuario(s).')
        except UsuarioError as exc:
            messages.error(request, str(exc))
        return redirect('usuarios:user_list')
