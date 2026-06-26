"""Modelos del módulo de Evaluaciones (núcleo).

Flujo: Evaluacion → Pregunta → Opcion ; Asignacion → Intento → Respuesta/Resultado.
La `Evaluacion` tiene una máquina de estados controlada por casos de uso.
"""

from django.conf import settings
from django.db import models


class Evaluacion(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADA = "publicada", "Publicada"
        ABIERTA = "abierta", "Abierta"
        CERRADA = "cerrada", "Cerrada"
        CANCELADA = "cancelada", "Cancelada"
        ARCHIVADA = "archivada", "Archivada"

    titulo = models.CharField("Título", max_length=180)
    descripcion = models.TextField("Descripción", blank=True, default="")
    area_tema = models.CharField("Área temática", max_length=120)
    nivel_riesgo = models.ForeignKey(
        "workers.NivelRiesgo", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="evaluaciones", verbose_name="Nivel de riesgo objetivo",
    )
    umbral_aprobacion = models.PositiveSmallIntegerField("Umbral de aprobación (%)", default=70)
    tiempo_limite_min = models.PositiveSmallIntegerField("Tiempo límite (min)", null=True, blank=True)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.BORRADOR)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="evaluaciones_creadas",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ["-creado_en"]

    def __str__(self):
        return self.titulo

    @property
    def editable(self):
        """Solo se puede editar / gestionar preguntas en borrador."""
        return self.estado == self.Estado.BORRADOR

    @property
    def admite_rendicion(self):
        return self.estado == self.Estado.ABIERTA


class Pregunta(models.Model):
    class Tipo(models.TextChoices):
        OPCION_MULTIPLE = "opcion_multiple", "Opción múltiple"
        VERDADERO_FALSO = "verdadero_falso", "Verdadero / Falso"

    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name="preguntas")
    enunciado = models.TextField("Enunciado")
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.OPCION_MULTIPLE)
    ponderacion = models.PositiveSmallIntegerField("Ponderación", default=1)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.enunciado[:60]


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="opciones")
    texto = models.CharField("Texto", max_length=240)
    es_correcta = models.BooleanField("Correcta", default=False)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.texto


class Asignacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        COMPLETADA = "completada", "Completada"
        VENCIDA = "vencida", "Vencida"

    class Origen(models.TextChoices):
        MANUAL = "manual", "Manual"
        AUTO_RIESGO = "auto_riesgo", "Automática por riesgo"

    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name="asignaciones")
    trabajador = models.ForeignKey("workers.Trabajador", on_delete=models.CASCADE, related_name="asignaciones")
    asignado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="asignaciones_creadas",
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)
    origen = models.CharField(max_length=12, choices=Origen.choices, default=Origen.MANUAL)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)

    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"
        ordering = ["-fecha_asignacion"]
        constraints = [
            models.UniqueConstraint(fields=["evaluacion", "trabajador"], name="uniq_eval_trabajador"),
        ]

    def __str__(self):
        return f"{self.evaluacion} → {self.trabajador}"


class Intento(models.Model):
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name="intentos")
    iniciado_en = models.DateTimeField(auto_now_add=True)
    enviado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Intento"
        verbose_name_plural = "Intentos"
        ordering = ["-iniciado_en"]


class Respuesta(models.Model):
    intento = models.ForeignKey(Intento, on_delete=models.CASCADE, related_name="respuestas")
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Opcion, on_delete=models.SET_NULL, null=True, blank=True)
    es_correcta = models.BooleanField(default=False)
    puntaje = models.PositiveSmallIntegerField(default=0)


class Resultado(models.Model):
    intento = models.OneToOneField(Intento, on_delete=models.CASCADE, related_name="resultado")
    puntaje_obtenido = models.PositiveSmallIntegerField(default=0)
    puntaje_total = models.PositiveSmallIntegerField(default=0)
    porcentaje = models.FloatField(default=0)
    aprobado = models.BooleanField(default=False)
    calificado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resultado"
        verbose_name_plural = "Resultados"

    def __str__(self):
        return f"{self.porcentaje:.0f}% ({'aprobado' if self.aprobado else 'reprobado'})"
