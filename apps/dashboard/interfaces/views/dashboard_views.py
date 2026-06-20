"""Vista del panel de control. Es el destino tras un login exitoso."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.dashboard.application.use_cases.get_summary import GetDashboardSummaryUseCase


class DashboardView(LoginRequiredMixin, View):
    """Página de inicio del sistema (requiere sesión activa)."""

    template_name = 'dashboard/index.html'

    def get(self, request):
        summary = GetDashboardSummaryUseCase().execute(request.user)
        return render(request, self.template_name, {'summary': summary})
