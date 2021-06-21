from django.views.generic import (
    FormView, TemplateView, RedirectView, ListView,
    CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.auth import get_user_model
from django.db.models import F, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from website.mixins import CheckAdminUserMixin
from .forms import (
    AdminLogin, UserGroupForm, AgentRegistrationForm, AgentProfileForm,
    AgentPasswordChangeForm, AgentWarehouseForm
)
from .constants import STAFF, AGENT
from .models import (
    Discipline, SubDiscipline, University, Degree,
    Designation, MedicineBrand, MedicineCompany
)
from warehouse.models import AgentProfile, WareHouse


class LoginView(FormView):
    template_name = 'core/admin/login.html'
    http_method_names = ['get', 'post']
    form_class = AdminLogin
    success_url = reverse_lazy('core:admin_dashboard')
    failure_url = reverse_lazy('core:admin_login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        user = authenticate(
            self.request,
            phone_number=form.cleaned_data['phone_number'],
            password=form.cleaned_data['password']
        )
        if user is None or user.user_type != STAFF or not user.is_active:
            messages.add_message(
                self.request, messages.ERROR, _('invalid_credentials')
            )
            return HttpResponseRedirect(self.failure_url)
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class Logout(RedirectView):
    url = reverse_lazy('core:admin_login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class Dashboard(CheckAdminUserMixin, TemplateView):
    template_name = 'core/admin/dashboard.html'
    login_url = reverse_lazy('core:admin_login')


class DisciplineList(CheckAdminUserMixin, ListView):
    model = Discipline
    template_name = 'core/discipline/discipline_list.html'
    context_object_name = 'disciplines'


class DisciplineCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Discipline
    fields = ('name', 'status', 'remark')
    template_name = 'core/discipline/discipline_form.html'
    success_url = reverse_lazy('core:discipline_list')
    success_message = 'Discipline was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Discipline'
        context['form_action'] = reverse_lazy('core:discipline_add')
        return context


class DisciplineUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Discipline
    fields = ('name', 'status', 'remark')
    template_name = 'core/discipline/discipline_form.html'
    success_url = reverse_lazy('core:discipline_list')
    success_message = 'Discipline was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Discipline - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'core:discipline_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class DisciplineDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Discipline
    http_method_names = ['get']
    success_url = reverse_lazy('core:discipline_list')
    success_message = 'Discipline was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class SubDisciplineList(CheckAdminUserMixin, ListView):
    model = SubDiscipline
    template_name = 'core/discipline/subdiscipline_list.html'
    context_object_name = 'disciplines'


class SubDisciplineCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = SubDiscipline
    fields = ('name', 'discipline', 'status', 'remark')
    template_name = 'core/discipline/subdiscipline_form.html'
    success_url = reverse_lazy('core:sub_discipline_list')
    success_message = 'Sub-Discipline was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Sub-Discipline'
        context['form_action'] = reverse_lazy('core:sub_discipline_add')
        return context


class SubDisciplineUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = SubDiscipline
    fields = ('name', 'discipline', 'status', 'remark')
    template_name = 'core/discipline/subdiscipline_form.html'
    success_url = reverse_lazy('core:sub_discipline_list')
    success_message = 'Sub-Discipline was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Sub-Discipline - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'core:sub_discipline_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class SubDisciplineDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = SubDiscipline
    http_method_names = ['get']
    success_url = reverse_lazy('core:sub_discipline_list')
    success_message = 'Sub-Discipline was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class UniversityList(CheckAdminUserMixin, ListView):
    model = University
    template_name = 'core/university/university_list.html'
    context_object_name = 'universities'


class UniversityCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = University
    fields = ('name', 'location', 'website_link', 'status', 'remark')
    template_name = 'core/university/university_form.html'
    success_url = reverse_lazy('core:university_list')
    success_message = 'University was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New University'
        context['form_action'] = reverse_lazy('core:university_add')
        return context


class UniversityUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = University
    fields = ('name', 'location', 'website_link', 'status', 'remark')
    template_name = 'core/university/university_form.html'
    success_url = reverse_lazy('core:university_list')
    success_message = 'University was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update University - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'core:university_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class UniversityDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = University
    http_method_names = ['get']
    success_url = reverse_lazy('core:university_list')
    success_message = 'University was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class DegreeList(CheckAdminUserMixin, ListView):
    model = Degree
    template_name = 'core/degree/degree_list.html'
    context_object_name = 'degrees'


class DegreeCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Degree
    fields = ('title', 'university', 'detail', 'status')
    template_name = 'core/degree/degree_form.html'
    success_url = reverse_lazy('core:degree_list')
    success_message = 'Degree was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Degree'
        context['form_action'] = reverse_lazy('core:degree_add')
        return context


class DegreeUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Degree
    fields = ('title', 'university', 'detail', 'status')
    template_name = 'core/degree/degree_form.html'
    success_url = reverse_lazy('core:degree_list')
    success_message = 'Degree was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Degree - ' + self.get_object().title
        context['form_action'] = reverse_lazy(
            'core:degree_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class DegreeDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Degree
    http_method_names = ['get']
    success_url = reverse_lazy('core:degree_list')
    success_message = 'Degree was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class DesignationList(CheckAdminUserMixin, ListView):
    model = Designation
    template_name = 'core/designation/designation_list.html'
    context_object_name = 'designations'


class DesignationCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Designation
    fields = ('title', 'status', 'remark')
    template_name = 'core/designation/designation_form.html'
    success_url = reverse_lazy('core:designation_list')
    success_message = 'Designation was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Designation'
        context['form_action'] = reverse_lazy('core:designation_add')
        return context


class DesignationUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Designation
    fields = ('title', 'status', 'remark')
    template_name = 'core/designation/designation_form.html'
    success_url = reverse_lazy('core:designation_list')
    success_message = 'Designation was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Designation - ' + self.get_object().title
        context['form_action'] = reverse_lazy(
            'core:designation_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class DesignationDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Designation
    http_method_names = ['get']
    success_url = reverse_lazy('core:designation_list')
    success_message = 'Designation was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


def get_university_via_degree(request):
    try:
        degree = Degree.objects.get(pk=request.POST.get('degree', None))
        if not None:
            universities = list(University.objects.filter(
                degree=degree).values('id', text=F('name')))
        return JsonResponse(universities, safe=False, status=200)
    except Exception:
        return JsonResponse(
            {'message': 'Invalid Request'}, status=400, safe=False
        )


class BrandList(CheckAdminUserMixin, ListView):
    model = MedicineBrand
    template_name = 'core/brand/brand_list.html'
    context_object_name = 'brands'


class BrandCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = MedicineBrand
    fields = ('name', 'status', 'remark')
    template_name = 'core/brand/brand_form.html'
    success_url = reverse_lazy('core:brand_list')
    success_message = 'Brand was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Brand'
        context['form_action'] = reverse_lazy('core:brand_add')
        return context


class BrandUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = MedicineBrand
    fields = ('name', 'status', 'remark')
    template_name = 'core/brand/brand_form.html'
    success_url = reverse_lazy('core:brand_list')
    success_message = 'Brand was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Brand - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'core:brand_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class BrandDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = MedicineBrand
    http_method_names = ['get']
    success_url = reverse_lazy('core:brand_list')
    success_message = 'Brand was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class ManufacturerList(CheckAdminUserMixin, ListView):
    model = MedicineCompany
    template_name = 'core/manufacturer/manufacturer_list.html'
    context_object_name = 'manufacturers'


class ManufacturerCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = MedicineCompany
    fields = ('name', 'status', 'remark')
    template_name = 'core/manufacturer/manufacturer_form.html'
    success_url = reverse_lazy('core:manufacturer_list')
    success_message = 'Manufacturer was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Manufacturer'
        context['form_action'] = reverse_lazy('core:manufacturer_add')
        return context


class ManufacturerUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = MedicineCompany
    fields = ('name', 'status', 'remark')
    template_name = 'core/manufacturer/manufacturer_form.html'
    success_url = reverse_lazy('core:manufacturer_list')
    success_message = 'Manufacturer was updated successfully'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Manufacturer - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'core:manufacturer_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class ManufacturerDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = MedicineCompany
    http_method_names = ['get']
    success_url = reverse_lazy('core:manufacturer_list')
    success_message = 'Manufacturer was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class GroupList(CheckAdminUserMixin, ListView):
    model = Group
    template_name = 'core/group/group_list.html'
    context_object_name = 'groups'


class GroupCreate(CheckAdminUserMixin, CreateView):
    model = Group
    form_class = UserGroupForm
    template_name = 'core/group/group_form.html'
    success_url = reverse_lazy('core:group_list')
    success_message = 'Group was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Group'
        context['form_action'] = reverse_lazy('core:group_add')
        return context


class GroupUpdate(CheckAdminUserMixin, UpdateView):
    model = Group
    form_class = UserGroupForm
    template_name = 'core/group/group_form.html'
    success_url = reverse_lazy('core:group_list')
    success_message = 'Group was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Group'
        context['form_action'] = reverse_lazy(
            'core:group_update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context


class AgentList(CheckAdminUserMixin, ListView):
    model = get_user_model()
    template_name = 'core/agent/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return AgentProfile.objects.select_related('user').all()


class AgentCreate(CheckAdminUserMixin, SuccessMessageMixin, FormView):
    template_name = 'core/agent/agent_form.html'
    form_class = AgentRegistrationForm

    def form_valid(self, form):
        with transaction.atomic():
            user = get_user_model().objects.create_user(
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],
                user_type=AGENT,
            )
            profile = AgentProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                designation=form.cleaned_data['designation'],
                location=form.cleaned_data['location'],
            )
        return HttpResponseRedirect(reverse_lazy(
            'core:agent_profile_update',
            kwargs={'pk': profile.pk}
        ))


class AgentProfileView(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = AgentProfile
    template_name = 'core/agent/agent_profile.html'
    form_class = AgentProfileForm
    context_object_name = 'profile'
    success_message = 'Profile Updated.'

    def get_success_url(self):
        return reverse_lazy(
            'core:agent_profile_update',
            kwargs={'pk': self.kwargs['pk']}
        )


class AgentChangePassword(CheckAdminUserMixin, SuccessMessageMixin, FormView):
    model = get_user_model()
    success_message = "Agent's Password Has Been Changed."
    template_name = 'core/agent/agent_password_form.html'
    form_class = AgentPasswordChangeForm
    success_url = reverse_lazy()

    def get_success_url(self):
        return reverse_lazy(
            'core:agent_password_change',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['agent'] = get_user_model().objects.get(
            pk=self.kwargs['pk']
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['password_confirmation']
            if password != confirmation:
                messages.add_message(
                    request, messages.ERROR,
                    'Password and password confirmation donot match'
                )
                return HttpResponseRedirect(self.get_success_url())
            user = get_user_model().objects.get(
                pk=self.kwargs['pk']
            )
            user.set_password(password)
            user.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Password changed'
            )
            return HttpResponseRedirect(self.get_success_url())


class AgentWarehouse(CheckAdminUserMixin, DetailView):
    template_name = 'core/agent/agent_warehouse_list.html'
    model = AgentProfile
    context_object_name = 'agent'


class AgentWarehouseCreate(CheckAdminUserMixin, UpdateView):
    model = AgentProfile
    form_class = AgentWarehouseForm
    template_name = 'core/agent/agent_warehouse_form.html'
    success_message = 'Warehouse was successfully assigned.'

    def get_success_url(self):
        return reverse_lazy(
            'core:agent_warehouse',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        current_warehouses = self.get_object().warehouse.values_list('pk')
        qs = WareHouse.objects.filter(
            ~Q(pk__in=current_warehouses)
        )
        kwargs.update({'qs': qs})
        return kwargs

    def form_valid(self, form):
        agent = self.get_object()
        current_warehouses = agent.warehouse.values_list('pk', flat=True)
        warehouses = [
            warehouse for warehouse in form.cleaned_data['warehouse']
            if warehouse.pk not in current_warehouses
        ]
        agent.warehouse.add(*warehouses)
        return HttpResponseRedirect(self.get_success_url())
