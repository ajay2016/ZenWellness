from django.views.generic import (
    TemplateView, ListView, FormView, RedirectView
)
from warehouse.models import Product
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from core.constants import (
    DOCTOR, AGENT, ONLINE_USER, PATIENT, LAB
)
from .mixins import CheckWebsiteUserMixin
from .forms import LoginForm


class Login(FormView):
    form_class = LoginForm
    template_name = 'website/auth/login.html'

    def _invalid_credentials(self):
        messages.add_message(
            self.request, messages.ERROR, 'Invalid Credentials',
            extra_tags='danger'
        )
        return HttpResponseRedirect(reverse_lazy('website:login'))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                user = get_user_model().objects.get(
                    phone_number=form.cleaned_data['phone_number']
                )
                if user.user_type not in [DOCTOR, AGENT, ONLINE_USER, PATIENT, LAB]:
                    return self._invalid_credentials()
                if not user.check_password(form.cleaned_data['password']):
                    return self._invalid_credentials()
                login(request, user)
                if user.user_type == DOCTOR:
                    return HttpResponseRedirect(
                        reverse_lazy('doctor:dashboard')
                    )
                elif user.user_type == AGENT:
                    return HttpResponseRedirect(
                        reverse_lazy('agent:dashbaord')
                    )
                elif user.user_type == ONLINE_USER:
                    return HttpResponseRedirect(
                        reverse_lazy('website:dashboard')
                    )
                elif user.user_type == PATIENT:
                    return HttpResponseRedirect(
                        reverse_lazy('patient:dashboard')
                    )
                elif user.user_type == LAB:
                    return HttpResponseRedirect(
                        reverse_lazy('lab:dashboard')
                    )
            except get_user_model().DoesNotExist:
                return self._invalid_credentials()


class Logout(RedirectView):
    url = reverse_lazy('website:login')

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        logout(request)
        return HttpResponseRedirect(url)


class LandingView(TemplateView):
    template_name = 'website/landing.html'


class MedicineView(ListView):
    model = Product
    template_name = 'website/medicine.html'
    context_object_name = 'products'


class Dashboard(CheckWebsiteUserMixin, TemplateView):
    template_name = 'website/dashboard.html'
