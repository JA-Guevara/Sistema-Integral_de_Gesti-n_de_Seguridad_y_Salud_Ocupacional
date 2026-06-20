"""Crea (o actualiza) los 4 roles base del proyecto con sus permisos.

Uso:  python manage.py seed_roles

Es idempotente: puede ejecutarse varias veces sin duplicar nada.
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from apps.usuarios.models import RolPerfil
from apps.usuarios.permissions_catalog import CODENAMES

# Definición de los roles base -> lista de codenames de permisos.
# '__all__' significa "todos los permisos del catálogo".
ROLES_BASE = {
    'Administrador': {
        'descripcion': 'Acceso total al sistema.',
        'permisos': '__all__',
    },
    'Responsable SySO': {
        'descripcion': 'Gestiona trabajadores, evaluaciones, capacitaciones y reportes.',
        'permisos': [
            'ver_usuarios',
            'ver_trabajadores', 'gestionar_trabajadores',
            'ver_evaluaciones', 'gestionar_evaluaciones',
            'ver_capacitaciones', 'gestionar_capacitaciones',
            'ver_reportes', 'gestionar_reportes',
            'ver_bitacora',
        ],
    },
    'Supervisor': {
        'descripcion': 'Consulta el desempeño y cumplimiento de los trabajadores.',
        'permisos': [
            'ver_trabajadores', 'ver_evaluaciones',
            'ver_capacitaciones', 'ver_reportes', 'ver_bitacora',
        ],
    },
    'Trabajador': {
        'descripcion': 'Realiza evaluaciones y consulta sus capacitaciones.',
        'permisos': ['ver_evaluaciones', 'ver_capacitaciones'],
    },
}


class Command(BaseCommand):
    help = 'Crea o actualiza los roles base del sistema con sus permisos.'

    def handle(self, *args, **options):
        permisos_por_codename = {
            p.codename: p for p in Permission.objects.filter(codename__in=CODENAMES)
        }
        if not permisos_por_codename:
            self.stderr.write(self.style.ERROR(
                'No hay permisos en BD. Ejecuta primero: python manage.py migrate'
            ))
            return

        for nombre, config in ROLES_BASE.items():
            grupo, creado = Group.objects.get_or_create(name=nombre)

            if config['permisos'] == '__all__':
                codenames = CODENAMES
            else:
                codenames = config['permisos']
            grupo.permissions.set(
                [permisos_por_codename[c] for c in codenames if c in permisos_por_codename]
            )

            RolPerfil.objects.update_or_create(
                grupo=grupo,
                defaults={'descripcion': config['descripcion'], 'activo': True},
            )

            estado = 'creado' if creado else 'actualizado'
            self.stdout.write(self.style.SUCCESS(
                f'  Rol "{nombre}" {estado} con {len(codenames)} permiso(s).'
            ))

        self.stdout.write(self.style.SUCCESS('Roles base listos.'))
