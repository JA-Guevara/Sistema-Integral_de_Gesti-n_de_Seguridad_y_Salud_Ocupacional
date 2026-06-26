"""Registro en el admin de Django de los catálogos y el padrón."""

from django.contrib import admin

from apps.workers.models import Area, Cargo, Empresa, NivelRiesgo, Trabajador


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'activo')
    search_fields = ('nombre', 'nit')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa')
    list_filter = ('empresa',)


admin.site.register(Cargo)
admin.site.register(NivelRiesgo)


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'documento', 'empresa', 'cargo', 'nivel_riesgo', 'estado')
    list_filter = ('empresa', 'area', 'nivel_riesgo', 'estado')
    search_fields = ('nombres', 'apellidos', 'documento')
