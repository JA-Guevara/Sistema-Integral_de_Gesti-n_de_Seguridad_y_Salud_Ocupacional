"""Casos de uso de ROLES (un Rol es un `auth.Group` + su RolPerfil)."""

from django.contrib.auth.models import Group, Permission

from apps.usuarios.application.use_cases.exceptions import UsuarioError
from apps.usuarios.models import RolPerfil
from apps.usuarios.permissions_catalog import CODENAMES


class ListarRoles:
    """Lista todos los roles con su perfil precargado."""

    def execute(self):
        return Group.objects.select_related('perfil').order_by('name')


class ObtenerRol:
    """Recupera un rol por id o lanza error de negocio."""

    def execute(self, rol_id):
        try:
            return Group.objects.select_related('perfil').get(pk=rol_id)
        except Group.DoesNotExist:
            raise UsuarioError('El rol solicitado no existe.')


def _permisos_validos(permission_ids):
    """Filtra los ids recibidos para aceptar SOLO permisos del catálogo."""
    return Permission.objects.filter(pk__in=permission_ids, codename__in=CODENAMES)


class CrearRol:
    """Crea un rol (Group), su perfil y le asigna permisos del catálogo."""

    def execute(self, *, nombre, descripcion, activo, permission_ids):
        nombre = (nombre or '').strip()
        if not nombre:
            raise UsuarioError('El nombre del rol es obligatorio.')
        if Group.objects.filter(name__iexact=nombre).exists():
            raise UsuarioError('Ya existe un rol con ese nombre.')

        grupo = Group.objects.create(name=nombre)
        RolPerfil.objects.create(grupo=grupo, descripcion=descripcion or '', activo=activo)
        grupo.permissions.set(_permisos_validos(permission_ids))
        return grupo


class ActualizarRol:
    """Actualiza nombre, descripción, estado y permisos de un rol."""

    def execute(self, rol_id, *, nombre, descripcion, activo, permission_ids):
        grupo = ObtenerRol().execute(rol_id)
        nombre = (nombre or '').strip()
        if not nombre:
            raise UsuarioError('El nombre del rol es obligatorio.')
        if Group.objects.filter(name__iexact=nombre).exclude(pk=grupo.pk).exists():
            raise UsuarioError('Ya existe otro rol con ese nombre.')

        grupo.name = nombre
        grupo.save(update_fields=['name'])

        perfil, _ = RolPerfil.objects.get_or_create(grupo=grupo)
        perfil.descripcion = descripcion or ''
        perfil.activo = activo
        perfil.save()

        grupo.permissions.set(_permisos_validos(permission_ids))
        return grupo


class CambiarEstadoRol:
    """Activa o desactiva un rol (alterna RolPerfil.activo)."""

    def execute(self, rol_id):
        grupo = ObtenerRol().execute(rol_id)
        perfil, _ = RolPerfil.objects.get_or_create(grupo=grupo)
        perfil.activo = not perfil.activo
        perfil.save(update_fields=['activo', 'actualizado_en'])
        return grupo
