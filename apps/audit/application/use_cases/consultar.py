"""Caso de uso de consulta de la bitácora (solo lectura)."""

from apps.audit.models import Auditoria


class ConsultarBitacora:
    def execute(self, *, modulo=None, accion=None, limite=500):
        qs = Auditoria.objects.select_related("usuario").all()
        if modulo:
            qs = qs.filter(modulo=modulo)
        if accion:
            qs = qs.filter(accion=accion)
        return qs[:limite]

    def modulos(self):
        return Auditoria.objects.values_list("modulo", flat=True).distinct().order_by("modulo")
