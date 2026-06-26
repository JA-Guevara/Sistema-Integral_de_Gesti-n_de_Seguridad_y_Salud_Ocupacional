"""Interfaz del proveedor de analítica (desacoplada de la implementación).

Permite cambiar el motor (reglas → LLM) sin tocar los casos de uso: basta
inyectar otra implementación de `IAnalyticsProvider` vía settings.
"""

from abc import ABC, abstractmethod


class IAnalyticsProvider(ABC):
    """Contrato del proveedor de diagnóstico de competencias."""

    @abstractmethod
    def detectar_brechas(self, niveles):
        """Recibe [{'area_tema': str, 'score': float}] y devuelve
        [{'area_tema': str, 'nivel_detectado': str, 'descripcion': str}]."""
        raise NotImplementedError

    @abstractmethod
    def recomendar(self, area_tema, score):
        """Devuelve un texto de recomendación para una brecha."""
        raise NotImplementedError
