"""Siembra los catálogos base del padrón (idempotente).

Uso:  python manage.py seed_workers

Crea los 4 niveles de riesgo y una empresa demo con áreas y cargos para que
el formulario de trabajadores sea usable de inmediato.
"""

from django.core.management.base import BaseCommand

from apps.workers.models import Area, Cargo, Empresa, NivelRiesgo

NIVELES = [('Bajo', 1), ('Medio', 2), ('Alto', 3), ('Crítico', 4)]
AREAS = ['Obra gruesa', 'Acabados', 'Instalaciones eléctricas', 'Seguridad e higiene']
CARGOS = ['Albañil', 'Ayudante', 'Electricista', 'Maestro de obra', 'Operador de maquinaria']


class Command(BaseCommand):
    help = 'Crea los catálogos base del padrón de trabajadores.'

    def handle(self, *args, **options):
        for nombre, orden in NIVELES:
            NivelRiesgo.objects.update_or_create(nombre=nombre, defaults={'orden': orden})
        self.stdout.write(self.style.SUCCESS(f'  {len(NIVELES)} niveles de riesgo listos.'))

        for nombre in CARGOS:
            Cargo.objects.get_or_create(nombre=nombre)
        self.stdout.write(self.style.SUCCESS(f'  {len(CARGOS)} cargos listos.'))

        empresa, _ = Empresa.objects.get_or_create(
            nombre='Constructora Demo S.R.L.',
            defaults={'nit': '1023456789', 'activo': True},
        )
        for nombre in AREAS:
            Area.objects.get_or_create(nombre=nombre, empresa=empresa)
        self.stdout.write(self.style.SUCCESS(
            f'  Empresa "{empresa.nombre}" con {len(AREAS)} áreas lista.'
        ))

        self.stdout.write(self.style.SUCCESS('Catálogos del padrón listos.'))
