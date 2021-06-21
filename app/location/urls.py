from django.urls import path
from .views import (
    CountryList, CountryCreate, CountryUpdate, CountryDelete,
    ProvinceList, ProvinceCreate, ProvinceUpdate, ProvinceDelete,
    ZoneList, ZoneCreate, ZoneUpdate, ZoneDelete, DistrictList,
    DistrictCreate, DistrictUpdate, DistrictDelete, LocationList,
    LocationCreate, LocationUpdate, LocationDelete
)

app_name = 'location'

urlpatterns = [
    path('country/', CountryList.as_view(), name="country_list"),
    path('country/create/', CountryCreate.as_view(), name="country_add"),
    path('country/update/<slug>', CountryUpdate.as_view(), name="country_update"),
    path('country/delete/<slug>', CountryDelete.as_view(), name="country_delete"),
    path('province/', ProvinceList.as_view(), name="province_list"),
    path('province/create/', ProvinceCreate.as_view(), name="province_add"),
    path('province/update/<slug>', ProvinceUpdate.as_view(), name="province_update"),
    path('province/delete/<slug>', ProvinceDelete.as_view(), name="province_delete"),
    path('zone/', ZoneList.as_view(), name="zone_list"),
    path('zone/create/', ZoneCreate.as_view(), name="zone_add"),
    path('zone/update/<slug>', ZoneUpdate.as_view(), name="zone_update"),
    path('zone/delete/<slug>', ZoneDelete.as_view(), name="zone_delete"),
    path('district/', DistrictList.as_view(), name="district_list"),
    path('district/create/', DistrictCreate.as_view(), name="district_add"),
    path('district/update/<slug>', DistrictUpdate.as_view(), name="district_update"),
    path('district/delete/<slug>', DistrictDelete.as_view(), name="district_delete"),
    path('location/', LocationList.as_view(), name="location_list"),
    path('location/create/', LocationCreate.as_view(), name="location_add"),
    path('location/update/<slug>', LocationUpdate.as_view(), name="location_update"),
    path('location/delete/<slug>', LocationDelete.as_view(), name="location_delete"),

]
