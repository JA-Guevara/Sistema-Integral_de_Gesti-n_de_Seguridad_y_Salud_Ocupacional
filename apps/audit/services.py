"""Servicio de auditoría + contexto de request (usuario/IP actuales).

El `CurrentRequestMiddleware` guarda el request en un thread-local; así los
receptores de señales pueden saber quién y desde qué IP ocurrió la acción.
"""

import threading

_local = threading.local()


def set_current_request(request):
    _local.request = request


def get_current_user():
    request = getattr(_local, "request", None)
    if request is not None and hasattr(request, "user"):
        user = request.user
        if getattr(user, "is_authenticated", False):
            return user
    return None


def get_current_ip():
    request = getattr(_local, "request", None)
    if request is None:
        return None
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def registrar_auditoria(accion, modulo, descripcion, usuario=None):
    """Crea un registro de auditoría (resiliente: nunca rompe el flujo)."""
    from apps.audit.models import Auditoria
    try:
        Auditoria.objects.create(
            usuario=usuario or get_current_user(),
            ip=get_current_ip(),
            accion=accion,
            modulo=modulo,
            descripcion=str(descripcion)[:240],
        )
    except Exception:
        # La auditoría jamás debe tumbar la operación de negocio.
        pass
