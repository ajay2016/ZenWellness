from django.urls import path
from .views import (
    Dashbaord, Warehouse, WareHouseDetail,
    WareHouseTransactionStockIn, WareHouseTrasactionStockOut,
    get_product_brands_company, get_product_rate_via_brand_company,
    get_product_quantity, WareHouseTrasactionSellToZenMembers,
    ListDoctors, ListPatients, CreatePatient, get_zone_via_province,
    get_district_via_zone, get_location_via_district,
    PatientConsellingQuestion, PatientConsellingFormList, UpdatePatient,
    CreatePatientCounselling, ApprovePatientConsellingForm, DoctorDetail,
    PatientConsellingFormView, LabTest, CreatePatientLabTest, get_tests_via_lab,
    get_doctor_appointment
)

app_name = 'agent'

urlpatterns = [
    path('', Dashbaord.as_view(), name='dashbaord'),
    path('warehouse/', Warehouse.as_view(), name='warehouse_list'),
    path('warehouse/<slug>', WareHouseDetail.as_view(), name='warehouse_detail'),
    path(
        'warehouse/<slug>/buy',
        WareHouseTransactionStockIn.as_view(),
        name='warehouse_transaction_buy'
    ),
    path(
        'sell/',
        WareHouseTrasactionStockOut.as_view(),
        name='warehouse_transaction_sell'
    ),
    path(
        'sell/zen-memebers/',
        WareHouseTrasactionSellToZenMembers.as_view(),
        name='warehouse_transaction_sell_to_members'
    ),
    path('sell/get-brands', get_product_brands_company, name="get_brands"),
    path('sell/get-rate', get_product_rate_via_brand_company, name="get_rate"),
    path('sell/calculate-quantity', get_product_quantity, name="get_product_quantity"),
    path('doctors/', ListDoctors.as_view(), name="list_doctors"),
    path('doctors/<pk>', DoctorDetail.as_view(), name="doctors_detail"),
    path('doctors/get-appointment/', get_doctor_appointment, name="doctors_appointments"),
    path('patients/', ListPatients.as_view(), name="list_patients"),
    path('patients/register/', CreatePatient.as_view(), name="add_patient"),
    path('patients/register/get-zone', get_zone_via_province, name="get_zone"),
    path('patients/register/get-district', get_district_via_zone, name="get_district"),
    path('patients/register/get-location', get_location_via_district, name="get_location"),
    path('patients/profile/<pk>/update', UpdatePatient.as_view(), name="update_patient"),
    path('patients/counselling/<pk>', PatientConsellingFormList.as_view(), name="patient_counselling_list"),
    path('patients/counselling/create/<pk>', CreatePatientCounselling.as_view(), name="patient_counselling_add"),
    path('patients/counselling/form/<pk>', PatientConsellingQuestion.as_view(), name="patient_counselling"),
    path('patients/counselling/form/<pk>/view', PatientConsellingFormView.as_view(), name="patient_counselling_form_view"),
    path('patients/counselling/form/<pk>/approve', ApprovePatientConsellingForm.as_view(), name="patient_counselling_approve"),
    path('patients/labs/<pk>', LabTest.as_view(), name="patient_lab_list"),
    path('patients/labs/schedule/<pk>', CreatePatientLabTest.as_view(), name="patient_lab_add"),
    path('patients/labs/tests/', get_tests_via_lab, name="get_lab_tests"),
]
