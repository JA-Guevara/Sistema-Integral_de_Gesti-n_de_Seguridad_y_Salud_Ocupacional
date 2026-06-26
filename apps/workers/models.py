"""Modelos del padrón de trabajadores.

El `Trabajador` es el eje del sistema: lo referencian (a futuro) las
evaluaciones, brechas, niveles de competencia y capacitaciones.
"""

from django.conf import settings
from django.db import models


class Empresa(models.Model):
    nombre = models.CharField('Nombre', max_length=160)
    nit = models.CharField('NIT', max_length=30, blank=True, default='')
    activo = models.BooleanField('Activa', default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Area(models.Model):
    nombre = models.CharField('Nombre', max_length=120)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='areas')

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    nombre = models.CharField('Nombre', max_length=120, unique=True)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class NivelRiesgo(models.Model):
    nombre = models.CharField('Nombre', max_length=40, unique=True)
    orden = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Nivel de riesgo'
        verbose_name_plural = 'Niveles de riesgo'
        ordering = ['orden']

    def __str__(self):
        return self.nombre

    @property
    def es_critico(self):
        return self.nombre in ('Alto', 'Crítico')


class Trabajador(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        INACTIVO = 'INACTIVO', 'Inactivo'

    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='trabajadores')
    nombres = models.CharField('Nombres', max_length=120)
    apellidos = models.CharField('Apellidos', max_length=120)
    documento = models.CharField('Documento de identidad', max_length=30, unique=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name='trabajadores')
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='trabajadores')
    nivel_riesgo = models.ForeignKey(NivelRiesgo, on_delete=models.PROTECT, related_name='trabajadores')
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='trabajadores_supervisados',
        verbose_name='Supervisor',
    )
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.apellidos}, {self.nombres}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'

    @property
    def activo(self):
        return self.estado == self.Estado.ACTIVO
