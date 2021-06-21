from django.views.generic import TemplateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from website.mixins import CheckPatientUserMixin
from healthcare.models import PatientProfile
from django.urls import reverse_lazy


class Dashboard(CheckPatientUserMixin, TemplateView):
    template_name = 'patient/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientProfile.objects.get(
            user=self.request.user
        )
        return context


class Profile(CheckPatientUserMixin, SuccessMessageMixin, UpdateView):
    model = PatientProfile
    template_name = 'patient/profile.html'
    fields = [
        'first_name', 'last_name', 'middle_name',
        'gender', 'date_of_birth'
    ]
    success_url = reverse_lazy('patient:profile')
    success_message = 'Profile Updated'

    def get_object(self, queryset=None):
        return PatientProfile.objects.get(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        # refactor ---> mixin or template
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientProfile.objects.get(
            user=self.request.user
        )
        return context
