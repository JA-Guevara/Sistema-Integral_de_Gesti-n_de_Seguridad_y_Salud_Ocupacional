"""Modelos de Capacitaciones.

El material se referencia por URL externa (no se almacenan videos). El flujo:
PlanCapacitacion → AsignacionCapacitacion (por trabajador) → Asistencia/avance.
"""

from django.conf import settings
from django.db import models


class PlanCapacitacion(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "activo", "Activo"
        CANCELADO = "cancelado", "Cancelado"

    titulo = models.CharField("Título", max_length=180)
    descripcion = models.TextField("Descripción", blank=True, default="")
    area_tema = models.CharField("Área temática", max_length=120)
    material_url = models.URLField("URL del material", blank=True, default="")
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="planes_creados",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plan de capacitación"
        verbose_name_plural = "Planes de capacitación"
        ordering = ["-creado_en"]

    def __str__(self):
        return self.titulo

    @property
    def activo(self):
        return self.estado == self.Estado.ACTIVO


class AsignacionCapacitacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_CURSO = "en_curso", "En curso"
        COMPLETADO = "completado", "Completado"
        CANCELADO = "cancelado", "Cancelado"

    plan = models.ForeignKey(PlanCapacitacion, on_delete=models.CASCADE, related_name="asignaciones")
    trabajador = models.ForeignKey("workers.Trabajador", on_delete=models.CASCADE, related_name="capacitaciones")
    brecha = models.ForeignKey(
        "analytics.Brecha", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="capacitaciones",
    )
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    avance_pct = models.PositiveSmallIntegerField("Avance (%)", default=0)
    asignado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="capacitaciones_asignadas",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asignación de capacitación"
        verbose_name_plural = "Asignaciones de capacitación"
        ordering = ["-creado_en"]
        constraints = [
            models.UniqueConstraint(fields=["plan", "trabajador"], name="uniq_plan_trabajador"),
        ]

    def __str__(self):
        return f"{self.plan} → {self.trabajador}"


class Asistencia(models.Model):
    asignacion = models.ForeignKey(AsignacionCapacitacion, on_delete=models.CASCADE, related_name="asistencias")
    fecha = models.DateField("Fecha")
    asistio = models.BooleanField("Asistió", default=True)
    observacion = models.CharField("Observación", max_length=240, blank=True, default="")
    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ["-fecha"]
