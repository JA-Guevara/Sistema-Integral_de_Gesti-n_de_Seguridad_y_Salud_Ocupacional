"""Excepciones de dominio del módulo de autenticación."""


class AuthError(Exception):
    """Error de negocio del módulo de autenticación.

    Su mensaje está pensado para mostrarse directamente al usuario final
    (vía Django Messages). Las vistas la capturan y la traducen a un mensaje.
    """
