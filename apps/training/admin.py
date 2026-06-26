from django.contrib import admin

from apps.training.models import Asistencia, AsignacionCapacitacion, PlanCapacitacion


@admin.register(PlanCapacitacion)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("titulo", "area_tema", "estado", "creado_en")
    list_filter = ("estado", "area_tema")


@admin.register(AsignacionCapacitacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ("plan", "trabajador", "estado", "avance_pct")
    list_filter = ("estado",)


admin.site.register(Asistencia)
