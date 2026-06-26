"""Modelo de Bitácora (append-only: no se edita ni borra desde la app)."""

from django.conf import settings
from django.db import models


class Auditoria(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="acciones_auditoria",
    )
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    accion = models.CharField("Acción", max_length=40)
    modulo = models.CharField("Módulo", max_length=60)
    descripcion = models.CharField("Descripción", max_length=240)

    class Meta:
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Bitácora"
        ordering = ["-fecha"]

    def __str__(self):
        return f"[{self.fecha:%Y-%m-%d %H:%M}] {self.accion} · {self.modulo}"
