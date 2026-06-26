"""Casos de uso del padrón de trabajadores."""

from apps.workers.application.use_cases.exceptions import WorkerError
from apps.workers.models import Empresa, Trabajador


class ListarTrabajadores:
    """Lista trabajadores con sus relaciones precargadas (evita N+1)."""

    def execute(self):
        return Trabajador.objects.select_related(
            'empresa', 'cargo', 'area', 'nivel_riesgo', 'supervisor'
        ).all()


class ObtenerTrabajador:
    """Recupera un trabajador por id o lanza error de negocio."""

    def execute(self, trabajador_id):
        try:
            return Trabajador.objects.select_related(
                'empresa', 'cargo', 'area', 'nivel_riesgo', 'supervisor'
            ).get(pk=trabajador_id)
        except Trabajador.DoesNotExist:
            raise WorkerError('El trabajador solicitado no existe.')


class RegistrarTrabajador:
    """Registra un trabajador a partir de un formulario ya validado."""

    def execute(self, form):
        return form.save()


class ActualizarTrabajador:
    """Actualiza los datos de un trabajador."""

    def execute(self, form):
        return form.save()


class CambiarEstadoTrabajador:
    """Activa o desactiva un trabajador (alterna su estado)."""

    def execute(self, trabajador_id):
        trabajador = ObtenerTrabajador().execute(trabajador_id)
        trabajador.estado = (
            Trabajador.Estado.INACTIVO if trabajador.activo else Trabajador.Estado.ACTIVO
        )
        trabajador.save(update_fields=['estado', 'actualizado_en'])
        return trabajador


class ResumenTrabajadores:
    """Calcula los indicadores (KPIs) del módulo para las tarjetas del listado."""

    def execute(self):
        qs = Trabajador.objects.all()
        return {
            'total': qs.count(),
            'activos': qs.filter(estado=Trabajador.Estado.ACTIVO).count(),
            'riesgo_alto': qs.filter(nivel_riesgo__nombre__in=['Alto', 'Crítico']).count(),
            'empresas': Empresa.objects.count(),
        }
