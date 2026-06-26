"""Casos de uso de asignación, avance y asistencia de capacitaciones."""

from apps.training.application.use_cases.exceptions import TrainingError
from apps.training.models import AsignacionCapacitacion, Asistencia
from apps.workers.models import Trabajador


class AsignarPlan:
    """Asigna un plan ACTIVO a uno o varios trabajadores (sin duplicar)."""

    def execute(self, plan, *, trabajador_ids, actor=None):
        if not plan.activo:
            raise TrainingError("No se puede asignar un plan cancelado.")
        trabajadores = Trabajador.objects.filter(pk__in=trabajador_ids, estado=Trabajador.Estado.ACTIVO)
        if not trabajadores.exists():
            raise TrainingError("Selecciona al menos un trabajador activo.")
        creadas = 0
        for trabajador in trabajadores:
            _, creada = AsignacionCapacitacion.objects.get_or_create(
                plan=plan, trabajador=trabajador, defaults={"asignado_por": actor},
            )
            creadas += int(creada)
        return creadas


class ObtenerAsignacion:
    def execute(self, asignacion_id):
        try:
            return AsignacionCapacitacion.objects.select_related("plan", "trabajador").get(pk=asignacion_id)
        except AsignacionCapacitacion.DoesNotExist:
            raise TrainingError("La asignación solicitada no existe.")


class RegistrarAvance:
    """Actualiza el avance (0–100). El estado se deriva del porcentaje."""

    def execute(self, asignacion_id, avance_pct):
        asignacion = ObtenerAsignacion().execute(asignacion_id)
        if asignacion.estado == AsignacionCapacitacion.Estado.CANCELADO:
            raise TrainingError("La asignación está cancelada.")
        try:
            pct = int(avance_pct)
        except (TypeError, ValueError):
            raise TrainingError("El avance debe ser un número.")
        if not (0 <= pct <= 100):
            raise TrainingError("El avance debe estar entre 0 y 100.")

        asignacion.avance_pct = pct
        if pct >= 100:
            asignacion.estado = AsignacionCapacitacion.Estado.COMPLETADO
        elif pct > 0:
            asignacion.estado = AsignacionCapacitacion.Estado.EN_CURSO
        else:
            asignacion.estado = AsignacionCapacitacion.Estado.PENDIENTE
        asignacion.save(update_fields=["avance_pct", "estado"])
        return asignacion


class MarcarCompletado:
    def execute(self, asignacion_id):
        asignacion = ObtenerAsignacion().execute(asignacion_id)
        if asignacion.estado == AsignacionCapacitacion.Estado.CANCELADO:
            raise TrainingError("No se puede completar una asignación cancelada.")
        asignacion.estado = AsignacionCapacitacion.Estado.COMPLETADO
        asignacion.avance_pct = 100
        asignacion.save(update_fields=["estado", "avance_pct"])
        return asignacion


class RegistrarAsistencia:
    def execute(self, asignacion_id, *, fecha, asistio, observacion=""):
        asignacion = ObtenerAsignacion().execute(asignacion_id)
        if not fecha:
            raise TrainingError("La fecha es obligatoria.")
        return Asistencia.objects.create(
            asignacion=asignacion, fecha=fecha, asistio=asistio, observacion=observacion or "",
        )
