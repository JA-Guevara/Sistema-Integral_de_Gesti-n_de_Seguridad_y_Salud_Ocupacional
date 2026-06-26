"""Vista de consulta de la bitácora (solo lectura)."""

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.audit.application.use_cases.consultar import ConsultarBitacora


class BitacoraListView(PermissionRequiredMixin, View):
    permission_required = "usuarios.ver_bitacora"
    raise_exception = True

    def get(self, request):
        uc = ConsultarBitacora()
        registros = uc.execute(
            modulo=request.GET.get("modulo") or None,
            accion=request.GET.get("accion") or None,
        )
        return render(request, "audit/bitacora.html", {
            "registros": registros,
            "modulos": uc.modulos(),
            "modulo_actual": request.GET.get("modulo") or "",
        })
