"""Modelos de Analítica: nivel de competencia, brechas y recomendaciones.

Una Brecha nace como `sugerida` (la genera la analítica) y solo el Responsable
SySO la pasa a `validada` o `descartada`. La analítica nunca cambia la aptitud.
"""

from django.conf import settings
from django.db import models


class NivelCompetencia(models.Model):
    trabajador = models.ForeignKey("workers.Trabajador", on_delete=models.CASCADE, related_name="niveles_competencia")
    area_tema = models.CharField("Área temática", max_length=120)
    score = models.FloatField("Puntaje de competencia (%)", default=0)
    calculado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nivel de competencia"
        verbose_name_plural = "Niveles de competencia"
        constraints = [
            models.UniqueConstraint(fields=["trabajador", "area_tema"], name="uniq_competencia_trab_area"),
        ]
        ordering = ["area_tema"]

    def __str__(self):
        return f"{self.trabajador} · {self.area_tema}: {self.score:.0f}%"


class Brecha(models.Model):
    class Estado(models.TextChoices):
        SUGERIDA = "sugerida", "Sugerida"
        VALIDADA = "validada", "Validada"
        DESCARTADA = "descartada", "Descartada"

    trabajador = models.ForeignKey("workers.Trabajador", on_delete=models.CASCADE, related_name="brechas")
    area_tema = models.CharField("Área temática", max_length=120)
    nivel_detectado = models.CharField("Nivel detectado", max_length=20)
    descripcion = models.CharField("Descripción", max_length=240)
    origen = models.CharField(max_length=20, default="analytics")
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.SUGERIDA)
    validada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="brechas_validadas",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brecha"
        verbose_name_plural = "Brechas"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.trabajador} · {self.area_tema} ({self.get_estado_display()})"


class Recomendacion(models.Model):
    brecha = models.OneToOneField(Brecha, on_delete=models.CASCADE, related_name="recomendacion")
    area_tema = models.CharField("Área temática", max_length=120)
    motivo = models.CharField("Motivo", max_length=240)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recomendación"
        verbose_name_plural = "Recomendaciones"

    def __str__(self):
        return f"Recomendación para {self.brecha}"
