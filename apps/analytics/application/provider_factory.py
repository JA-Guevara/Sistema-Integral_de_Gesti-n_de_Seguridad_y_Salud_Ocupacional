"""Fábrica que resuelve el proveedor de analítica según settings.

Por defecto usa el proveedor basado en reglas. Para cambiarlo, define en
settings:  ANALYTICS_PROVIDER = "ruta.al.Modulo.Clase".
"""

from django.conf import settings
from django.utils.module_loading import import_string

DEFAULT_PROVIDER = "apps.analytics.infrastructure.providers.rule_based.RuleBasedAnalyticsProvider"


def get_analytics_provider():
    ruta = getattr(settings, "ANALYTICS_PROVIDER", DEFAULT_PROVIDER)
    provider_class = import_string(ruta)
    return provider_class()
