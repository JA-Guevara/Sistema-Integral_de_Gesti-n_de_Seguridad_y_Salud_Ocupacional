"""Proveedor de analítica basado en REGLAS (implementación inicial).

Es 100% determinista y auditable. Se puede reemplazar por un proveedor
basado en LLM sin tocar los casos de uso (ver `get_analytics_provider`).
"""

from apps.analytics.domain.services.provider import IAnalyticsProvider

UMBRAL_BRECHA = 70   # competencia mínima esperada (%)
UMBRAL_CRITICO = 50  # por debajo de esto, la brecha es crítica


class RuleBasedAnalyticsProvider(IAnalyticsProvider):
    def detectar_brechas(self, niveles):
        brechas = []
        for nivel in niveles:
            score = nivel["score"]
            if score < UMBRAL_BRECHA:
                detectado = "Crítico" if score < UMBRAL_CRITICO else "Bajo"
                brechas.append({
                    "area_tema": nivel["area_tema"],
                    "nivel_detectado": detectado,
                    "descripcion": f"Competencia {score:.0f}% en «{nivel['area_tema']}», "
                                   f"por debajo del umbral del {UMBRAL_BRECHA}%.",
                })
        return brechas

    def recomendar(self, area_tema, score):
        return (f"Asignar capacitación de refuerzo en «{area_tema}» "
                f"(competencia actual {score:.0f}%).")
