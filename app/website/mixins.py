from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from core.constants import DOCTOR, AGENT, STAFF, ONLINE_USER, PATIENT, LAB


class DoctorLoginRequiredMixin(AccessMixin):
    login_url = '/auth/login/'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is authenticated and is a doctor."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != DOCTOR:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('website:login'))
        return super().dispatch(request, *args, **kwargs)


class AgentLoginRequiredMixin(AccessMixin):
    login_url = '/auth/login/'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is authenticated and is an agent."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != AGENT:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('website:login'))
        return super().dispatch(request, *args, **kwargs)


class CheckAdminUserMixin(AccessMixin):
    login_url = '/admin/login/'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is admin user."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != STAFF:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('core:admin_login'))
        return super().dispatch(request, *args, **kwargs)


class CheckWebsiteUserMixin(AccessMixin):
    login_url = '/auth/login/'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is admin user."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != ONLINE_USER:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('website:login'))
        return super().dispatch(request, *args, **kwargs)


class CheckPatientUserMixin(AccessMixin):
    login_url = '/auth/login/'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is admin user."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != PATIENT:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('website:login'))
        return super().dispatch(request, *args, **kwargs)


class CheckLabAgentUserMixin(AccessMixin):
    login_url = '/auth/login/'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is lab user."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != LAB:
            logout(request)
            return HttpResponseRedirect(reverse_lazy('website:login'))
        return super().dispatch(request, *args, **kwargs)
