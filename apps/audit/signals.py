"""Receptores de señales que alimentan la bitácora automáticamente.

Audita la creación/edición/eliminación de los modelos críticos y los
inicios/cierres de sesión, capturando el usuario e IP desde el request.
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.audit.services import registrar_auditoria

# app_label -> nombre de módulo legible para la bitácora.
MODULOS = {
    "workers": "Trabajadores",
    "evaluations": "Evaluaciones",
    "analytics": "Analítica",
    "training": "Capacitaciones",
    "usuarios": "Roles y permisos",
    "auth": "Usuarios",
}

# Modelos cuyas mutaciones se auditan.
MODELOS_AUDITADOS = {
    "Trabajador", "Evaluacion", "PlanCapacitacion", "Brecha",
    "Group", "AsignacionCapacitacion", "RolPerfil",
}


def _modulo(sender):
    return MODULOS.get(sender._meta.app_label, sender._meta.app_label)


@receiver(post_save)
def log_guardado(sender, instance, created, **kwargs):
    nombre = sender.__name__
    if nombre == "User":
        # Solo la creación de usuarios (evita ruido por last_login en cada login).
        if created:
            registrar_auditoria("Creación", "Usuarios", f"Se creó el usuario {instance}")
        return
    if nombre not in MODELOS_AUDITADOS:
        return
    accion = "Creación" if created else "Edición"
    registrar_auditoria(accion, _modulo(sender), f"{accion} de {sender._meta.verbose_name}: {instance}")


@receiver(post_delete)
def log_eliminado(sender, instance, **kwargs):
    nombre = sender.__name__
    if nombre not in MODELOS_AUDITADOS and nombre != "User":
        return
    modulo = "Usuarios" if nombre == "User" else _modulo(sender)
    registrar_auditoria("Eliminación", modulo, f"Eliminación de {sender._meta.verbose_name}: {instance}")


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    registrar_auditoria("Inicio de sesión", "Autenticación", f"{user} inició sesión", usuario=user)


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user is not None:
        registrar_auditoria("Cierre de sesión", "Autenticación", f"{user} cerró sesión", usuario=user)
