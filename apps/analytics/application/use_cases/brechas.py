"""Casos de uso de gestión de brechas (listar y validar/descartar)."""

from apps.analytics.application.provider_factory import get_analytics_provider
from apps.analytics.application.use_cases.exceptions import AnalyticsError
from apps.analytics.models import Brecha, NivelCompetencia, Recomendacion


class ListarBrechas:
    def execute(self, estado=None):
        qs = Brecha.objects.select_related("trabajador").all()
        if estado:
            qs = qs.filter(estado=estado)
        return qs


class ValidarBrecha:
    """ÚNICO punto que da por buena (o descarta) una brecha — acción humana.

    Al validar, genera una Recomendación de capacitación (vía proveedor).
    """

    def __init__(self, provider=None):
        self.provider = provider or get_analytics_provider()

    def execute(self, brecha_id, decision, actor=None):
        try:
            brecha = Brecha.objects.get(pk=brecha_id)
        except Brecha.DoesNotExist:
            raise AnalyticsError("La brecha solicitada no existe.")

        if brecha.estado != Brecha.Estado.SUGERIDA:
            raise AnalyticsError("Solo se pueden validar o descartar brechas sugeridas.")

        if decision == "validar":
            brecha.estado = Brecha.Estado.VALIDADA
            brecha.validada_por = actor
            brecha.save(update_fields=["estado", "validada_por", "actualizado_en"])
            self._crear_recomendacion(brecha)
        elif decision == "descartar":
            brecha.estado = Brecha.Estado.DESCARTADA
            brecha.validada_por = actor
            brecha.save(update_fields=["estado", "validada_por", "actualizado_en"])
        else:
            raise AnalyticsError("Decisión inválida.")
        return brecha

    def _crear_recomendacion(self, brecha):
        nivel = NivelCompetencia.objects.filter(
            trabajador=brecha.trabajador, area_tema=brecha.area_tema
        ).first()
        score = nivel.score if nivel else 0
        Recomendacion.objects.get_or_create(
            brecha=brecha,
            defaults={
                "area_tema": brecha.area_tema,
                "motivo": self.provider.recomendar(brecha.area_tema, score),
            },
        )
