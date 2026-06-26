from django.contrib import admin

from apps.analytics.models import Brecha, NivelCompetencia, Recomendacion


@admin.register(Brecha)
class BrechaAdmin(admin.ModelAdmin):
    list_display = ("trabajador", "area_tema", "nivel_detectado", "estado", "creado_en")
    list_filter = ("estado", "area_tema")


admin.site.register(NivelCompetencia)
admin.site.register(Recomendacion)
