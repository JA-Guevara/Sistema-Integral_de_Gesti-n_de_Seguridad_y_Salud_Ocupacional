"""Vistas de administración de ROLES."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.usuarios.application.use_cases.exceptions import UsuarioError
from apps.usuarios.application.use_cases.permissions import listar_permisos_agrupados
from apps.usuarios.application.use_cases.roles import (
    ActualizarRol,
    CambiarEstadoRol,
    CrearRol,
    ListarRoles,
    ObtenerRol,
)
from apps.usuarios.interfaces.forms.rol_form import RolForm


class RolListView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.ver_roles'
    raise_exception = True

    def get(self, request):
        return render(request, 'usuarios/roles/lista.html', {
            'roles': ListarRoles().execute(),
        })


class RolCreateView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_roles'
    raise_exception = True

    def get(self, request):
        return self._render(request, RolForm(initial={'active': True}), seleccionados=[])

    def post(self, request):
        form = RolForm(request.POST)
        permission_ids = request.POST.getlist('permissions')
        if form.is_valid():
            try:
                rol = CrearRol().execute(
                    nombre=form.cleaned_data['name'],
                    descripcion=form.cleaned_data['description'],
                    activo=form.cleaned_data['active'],
                    permission_ids=permission_ids,
                )
                messages.success(request, 'Rol creado correctamente.')
                return redirect('usuarios:rol_detail', pk=rol.pk)
            except UsuarioError as exc:
                messages.error(request, str(exc))
        return self._render(request, form, seleccionados=[int(x) for x in permission_ids])

    def _render(self, request, form, seleccionados):
        return render(request, 'usuarios/roles/form.html', {
            'form': form,
            'rol': None,
            'permisos_agrupados': listar_permisos_agrupados(),
            'seleccionados': seleccionados,
        })


class RolUpdateView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_roles'
    raise_exception = True

    def get(self, request, pk):
        rol = ObtenerRol().execute(pk)
        perfil = getattr(rol, 'perfil', None)
        form = RolForm(initial={
            'name': rol.name,
            'description': perfil.descripcion if perfil else '',
            'active': perfil.activo if perfil else True,
        })
        seleccionados = list(rol.permissions.values_list('id', flat=True))
        return self._render(request, form, rol, seleccionados)

    def post(self, request, pk):
        rol = ObtenerRol().execute(pk)
        form = RolForm(request.POST)
        permission_ids = request.POST.getlist('permissions')
        if form.is_valid():
            try:
                ActualizarRol().execute(
                    pk,
                    nombre=form.cleaned_data['name'],
                    descripcion=form.cleaned_data['description'],
                    activo=form.cleaned_data['active'],
                    permission_ids=permission_ids,
                )
                messages.success(request, 'Rol actualizado correctamente.')
                return redirect('usuarios:rol_detail', pk=pk)
            except UsuarioError as exc:
                messages.error(request, str(exc))
        return self._render(request, form, rol, [int(x) for x in permission_ids])

    def _render(self, request, form, rol, seleccionados):
        return render(request, 'usuarios/roles/form.html', {
            'form': form,
            'rol': rol,
            'permisos_agrupados': listar_permisos_agrupados(),
            'seleccionados': seleccionados,
        })


class RolDetailView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.ver_roles'
    raise_exception = True

    def get(self, request, pk):
        rol = ObtenerRol().execute(pk)
        return render(request, 'usuarios/roles/detalle.html', {
            'rol': rol,
            'perfil': getattr(rol, 'perfil', None),
            'permisos': rol.permissions.order_by('name'),
            'usuarios': rol.user_set.order_by('first_name', 'last_name'),
        })


class RolToggleView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_roles'
    raise_exception = True

    def post(self, request, pk):
        try:
            CambiarEstadoRol().execute(pk)
            messages.success(request, 'Estado del rol actualizado correctamente.')
        except UsuarioError as exc:
            messages.error(request, str(exc))
        return redirect('usuarios:rol_list')
