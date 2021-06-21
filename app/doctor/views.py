from django.views.generic import TemplateView
from website.mixins import DoctorLoginRequiredMixin


class Dashboard(DoctorLoginRequiredMixin, TemplateView):
    template_name = 'doctor/dashboard.html'
