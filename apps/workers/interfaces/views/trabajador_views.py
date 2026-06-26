"""Vistas del padrón de trabajadores (protegidas por permisos del catálogo)."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.workers.application.use_cases.exceptions import WorkerError
from apps.workers.application.use_cases.trabajadores import (
    ActualizarTrabajador,
    CambiarEstadoTrabajador,
    ListarTrabajadores,
    ObtenerTrabajador,
    RegistrarTrabajador,
    ResumenTrabajadores,
)
from apps.workers.interfaces.forms.trabajador_form import TrabajadorForm


class TrabajadorListView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.ver_trabajadores'
    raise_exception = True

    def get(self, request):
        return render(request, 'workers/trabajadores/lista.html', {
            'trabajadores': ListarTrabajadores().execute(),
            'resumen': ResumenTrabajadores().execute(),
        })


class TrabajadorCreateView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_trabajadores'
    raise_exception = True

    def get(self, request):
        return render(request, 'workers/trabajadores/form.html', {
            'form': TrabajadorForm(), 'trabajador': None,
        })

    def post(self, request):
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            trabajador = RegistrarTrabajador().execute(form)
            messages.success(request, 'Trabajador registrado correctamente.')
            return redirect('workers:trabajador_detail', pk=trabajador.pk)
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, 'workers/trabajadores/form.html', {'form': form, 'trabajador': None})


class TrabajadorUpdateView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_trabajadores'
    raise_exception = True

    def get(self, request, pk):
        trabajador = ObtenerTrabajador().execute(pk)
        return render(request, 'workers/trabajadores/form.html', {
            'form': TrabajadorForm(instance=trabajador), 'trabajador': trabajador,
        })

    def post(self, request, pk):
        trabajador = ObtenerTrabajador().execute(pk)
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid():
            ActualizarTrabajador().execute(form)
            messages.success(request, 'Trabajador actualizado correctamente.')
            return redirect('workers:trabajador_detail', pk=pk)
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, 'workers/trabajadores/form.html', {'form': form, 'trabajador': trabajador})


class TrabajadorDetailView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.ver_trabajadores'
    raise_exception = True

    def get(self, request, pk):
        trabajador = ObtenerTrabajador().execute(pk)
        return render(request, 'workers/trabajadores/detalle.html', {'trabajador': trabajador})


class TrabajadorToggleView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.gestionar_trabajadores'
    raise_exception = True

    def post(self, request, pk):
        try:
            CambiarEstadoTrabajador().execute(pk)
            messages.success(request, 'Estado del trabajador actualizado correctamente.')
        except WorkerError as exc:
            messages.error(request, str(exc))
        return redirect('workers:trabajador_list')
