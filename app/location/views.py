from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from website.mixins import CheckAdminUserMixin
from .models import (
    Country, Province, Zone, District, Location
)


class CountryList(CheckAdminUserMixin, ListView):
    model = Country
    context_object_name = 'countries'


class CountryCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Country
    fields = ('name', 'status')
    success_url = reverse_lazy('location:country_list')
    success_message = "A New Country Has Been Added To The Country List."

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Country'
        context['form_action'] = reverse_lazy('location:country_add')
        return context


class CountryUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Country
    fields = ('name', 'status')
    success_url = reverse_lazy('location:country_list')
    success_message = "Country Information Has Been Updated."
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Update Country' + self.get_object().name
        context['form_action'] = reverse_lazy(
                'location:country_update',
                kwargs={'slug': self.get_object().name}
            )
        return context


class CountryDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Country
    success_url = reverse_lazy('location:country_list')
    success_message = "Country Has Been Removed."
    slug_field = 'name'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class ProvinceList(CheckAdminUserMixin, ListView):
    model = Province
    context_object_name = 'provinces'


class ProvinceCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Province
    fields = ('name', 'country', 'status')
    success_url = reverse_lazy('location:province_list')
    success_message = "A New Province Has Been Added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Province'
        context['form_action'] = reverse_lazy('location:province_add')
        return context


class ProvinceUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Province
    fields = ('name', 'country', 'status')
    success_url = reverse_lazy('location:province_list')
    success_message = "Province Information Has Been Updated."
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Update Province' + self.get_object().name
        context['form_action'] = reverse_lazy(
                'location:province_update',
                kwargs={'slug': self.get_object().name}
            )
        return context


class ProvinceDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Province
    success_url = reverse_lazy('location:province_list')
    success_message = "Province Has Been Removed."
    slug_field = 'name'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class ZoneList(CheckAdminUserMixin, ListView):
    model = Zone
    context_object_name = 'zones'


class ZoneCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Zone
    fields = ('name', 'province', 'status')
    success_url = reverse_lazy('location:zone_list')
    success_message = "A New Zone Has Been Added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Zone'
        context['form_action'] = reverse_lazy('location:zone_add')
        return context


class ZoneUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Zone
    fields = ('name', 'province', 'status')
    success_url = reverse_lazy('location:zone_list')
    success_message = "Zone Information Has Been Updated."
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Update Zone' + self.get_object().name
        context['form_action'] = reverse_lazy(
                'location:zone_update',
                kwargs={'slug': self.get_object().name}
            )
        return context


class ZoneDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Zone
    success_url = reverse_lazy('location:zone_list')
    success_message = "Zone Has Been Removed."
    slug_field = 'name'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class DistrictList(CheckAdminUserMixin, ListView):
    model = District
    context_object_name = 'districts'


class DistrictCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = District
    fields = ('name', 'zone', 'status')
    success_url = reverse_lazy('location:district_list')
    success_message = "A New District Has Been Added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New District'
        context['form_action'] = reverse_lazy('location:district_add')
        return context


class DistrictUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = District
    fields = ('name', 'zone', 'status')
    success_url = reverse_lazy('location:district_list')
    success_message = "District Information Has Been Updated."
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'District Zone' + self.get_object().name
        context['form_action'] = reverse_lazy(
                'location:district_update',
                kwargs={'slug': self.get_object().name}
            )
        return context


class DistrictDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = District
    success_url = reverse_lazy('location:district_list')
    success_message = "Disctrict Has Been Removed."
    slug_field = 'name'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class LocationList(CheckAdminUserMixin, ListView):
    model = Location
    context_object_name = 'locations'


class LocationCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Location
    fields = ('name', 'district', 'status')
    success_url = reverse_lazy('location:location_list')
    success_message = "A New Location Has Been Added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Location'
        context['form_action'] = reverse_lazy('location:location_add')
        return context


class LocationUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Location
    fields = ('name', 'district', 'status')
    success_url = reverse_lazy('location:location_list')
    success_message = "Location Information Has Been Updated."
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'District Location' + self.get_object().name
        context['form_action'] = reverse_lazy(
                'location:location_update',
                kwargs={'slug': self.get_object().name}
            )
        return context


class LocationDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('location:location_list')
    success_message = "Location Has Been Removed."
    slug_field = 'name'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)
