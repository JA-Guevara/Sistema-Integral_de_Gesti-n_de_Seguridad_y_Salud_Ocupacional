"""Modelos del módulo de Usuarios, Roles y Permisos.

NO se redefine User ni se reemplaza el sistema de Groups/Permissions de Django.
Solo se agregan dos piezas:

  - RolPerfil: amplía un `Group` (= Rol) con descripción, estado activo y fechas.
  - ControlAcceso: modelo "fantasma" (sin tabla) que SOLO sirve para declarar
    los permisos por módulo del sistema como permisos nativos de Django.
"""

from django.contrib.auth.models import Group
from django.db import models

from apps.usuarios.permissions_catalog import PERMISSION_CATALOG


class RolPerfil(models.Model):
    """Datos adicionales de un Rol (Group de Django)."""

    grupo = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Rol',
    )
    descripcion = models.TextField('Descripción', blank=True, default='')
    activo = models.BooleanField('Activo', default=True)
    creado_en = models.DateTimeField('Creado en', auto_now_add=True)
    actualizado_en = models.DateTimeField('Actualizado en', auto_now=True)

    class Meta:
        verbose_name = 'Perfil de rol'
        verbose_name_plural = 'Perfiles de rol'

    def __str__(self):
        return f'Perfil de {self.grupo.name}'


class ControlAcceso(models.Model):
    """Modelo sin tabla (`managed = False`) usado SOLO para declarar permisos.

    Django crea un `auth.Permission` por cada entrada de `permissions` al correr
    las migraciones. Así obtenemos permisos por módulo sin tener que atarlos a
    un modelo CRUD concreto (que todavía no existe).
    """

    class Meta:
        managed = False          # no crea tabla en la base de datos
        default_permissions = ()  # sin add/change/delete/view automáticos
        permissions = [
            (item['codename'], item['descripcion']) for item in PERMISSION_CATALOG
        ]
