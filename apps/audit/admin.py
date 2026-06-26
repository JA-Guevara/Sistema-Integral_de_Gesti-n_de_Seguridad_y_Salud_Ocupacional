"""La bitácora es de solo lectura también en el admin (append-only)."""

from django.contrib import admin

from apps.audit.models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "usuario", "accion", "modulo", "descripcion", "ip")
    list_filter = ("modulo", "accion")
    search_fields = ("descripcion", "usuario__username")
    readonly_fields = ("usuario", "fecha", "ip", "accion", "modulo", "descripcion")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
