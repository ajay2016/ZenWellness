from django.views.generic import (
    TemplateView
)
from healthcare.models import (
    LabAgentProfile
)
from website.mixins import CheckLabAgentUserMixin


class Dashboard(CheckLabAgentUserMixin, TemplateView):
    template_name = 'lab/dashboard.html'


class TestList(CheckLabAgentUserMixin, TemplateView):
    template_name = 'lab/test_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab_agent = LabAgentProfile.objects.get(user=self.request.user)
        context['tests'] = lab_agent.lab.tests.all()
        return context
