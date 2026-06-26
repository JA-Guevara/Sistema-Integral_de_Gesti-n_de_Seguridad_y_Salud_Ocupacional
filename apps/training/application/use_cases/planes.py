"""Casos de uso de planes de capacitación."""

from django.db.models import Count

from apps.training.application.use_cases.exceptions import TrainingError
from apps.training.models import AsignacionCapacitacion, PlanCapacitacion


class ListarPlanes:
    def execute(self):
        return PlanCapacitacion.objects.annotate(
            n_asignaciones=Count("asignaciones", distinct=True),
        )


class ObtenerPlan:
    def execute(self, plan_id):
        try:
            return PlanCapacitacion.objects.get(pk=plan_id)
        except PlanCapacitacion.DoesNotExist:
            raise TrainingError("El plan solicitado no existe.")


class CrearPlan:
    def execute(self, form, actor=None):
        plan = form.save(commit=False)
        plan.creado_por = actor
        plan.save()
        return plan


class EditarPlan:
    def execute(self, form):
        return form.save()


class CancelarPlan:
    def execute(self, plan_id):
        plan = ObtenerPlan().execute(plan_id)
        plan.estado = PlanCapacitacion.Estado.CANCELADO
        plan.save(update_fields=["estado", "actualizado_en"])
        return plan


class ResumenCapacitaciones:
    def execute(self):
        asignaciones = AsignacionCapacitacion.objects.all()
        return {
            "planes": PlanCapacitacion.objects.filter(estado=PlanCapacitacion.Estado.ACTIVO).count(),
            "asignaciones": asignaciones.count(),
            "en_curso": asignaciones.filter(estado=AsignacionCapacitacion.Estado.EN_CURSO).count(),
            "completadas": asignaciones.filter(estado=AsignacionCapacitacion.Estado.COMPLETADO).count(),
        }
