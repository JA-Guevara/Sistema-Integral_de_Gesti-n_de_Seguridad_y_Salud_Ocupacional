from django.contrib import admin

from apps.evaluations.models import (
    Asignacion, Evaluacion, Intento, Opcion, Pregunta, Respuesta, Resultado,
)


class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 0


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("enunciado", "evaluacion", "tipo", "ponderacion")
    inlines = [OpcionInline]


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "area_tema", "estado", "umbral_aprobacion", "creado_en")
    list_filter = ("estado", "area_tema")
    search_fields = ("titulo", "area_tema")


admin.site.register(Asignacion)
admin.site.register(Intento)
admin.site.register(Respuesta)
admin.site.register(Resultado)
