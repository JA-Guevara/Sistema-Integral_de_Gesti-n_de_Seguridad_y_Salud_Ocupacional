"""Caso de uso: listar los permisos del catálogo agrupados por módulo."""

from collections import OrderedDict

from django.contrib.auth.models import Permission

from apps.usuarios.permissions_catalog import CODENAMES, PERMISSION_CATALOG


def listar_permisos_agrupados():
    """Devuelve un OrderedDict {modulo: [ {permission, accion, descripcion} ]}.

    Respeta el orden del catálogo y solo incluye permisos ya creados en BD.
    """
    permisos_bd = {
        p.codename: p
        for p in Permission.objects.filter(codename__in=CODENAMES)
    }

    agrupados = OrderedDict()
    for item in PERMISSION_CATALOG:
        permiso = permisos_bd.get(item['codename'])
        if permiso is None:
            continue  # aún no migrado
        agrupados.setdefault(item['modulo'], []).append({
            'permission': permiso,
            'accion': item['accion'],
            'descripcion': item['descripcion'],
        })
    return agrupados
