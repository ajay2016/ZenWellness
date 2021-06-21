import datetime
import uuid
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView,
    FormView, UpdateView
)
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib import messages
from django.urls import reverse_lazy
from website.mixins import AgentLoginRequiredMixin
from warehouse.models import (
    AgentProfile, WareHouse, ProductTransaction,
    Product
)
from healthcare.models import DoctorProfile, PatientProfile
from core.constants import STAFF, PATIENT
from core.models import MedicineBrand, MedicineCompany, SubDiscipline
from location.models import Province, Zone, District, Location
from healthcare.models import (
    PatientConsellingQuestionResult, Question, QuestionChoices,
    ConsellingQuestionSetsAnswers, PatientConsellingQuestionResult,
    PatientLabTest, Labs, LabTests, DoctorVistingSchedules, Organization
)
from .forms import (
    WareHouseTransactionForm, PatientRegistrationForm,
    PatientConsellingQuestionForm
)


class Dashbaord(AgentLoginRequiredMixin, TemplateView):
    template_name = 'agent/dashboard.html'


class Warehouse(AgentLoginRequiredMixin, ListView):
    model = AgentProfile
    context_object_name = 'warehouses'
    template_name = 'agent/warehouse_list.html'

    def get_queryset(self):
        qs = AgentProfile.objects.get(
            user=self.request.user
        ).warehouse.prefetch_related('product_set').all()
        return qs


class WareHouseDetail(AgentLoginRequiredMixin, DetailView):
    model = WareHouse
    context_object_name = 'warehouse'
    template_name = 'agent/warehouse_deatil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = ProductTransaction.objects.filter(
            product__warehouse=self.get_object(),
            user=self.request.user
        ).order_by('-id')
        low_stock_orders = ProductTransaction.objects.raw(
            """SELECT
                ANY_VALUE(id) as id, product_id, company_id, brand_id,
                SUM(
                CASE WHEN transaction_type='I' then quantity
                WHEN transaction_type='O' then -quantity END
                ) as total
            FROM
                warehouse_producttransaction
            WHERE user_id = %s
            GROUP BY product_id, company_id, brand_id HAVING total <7;""",
            [self.request.user.pk])
        context['transactions'] = transactions
        context['low_stock_orders'] = low_stock_orders
        return context


class WareHouseTransactionStockIn(AgentLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProductTransaction
    template_name = 'agent/warehouse_transaction_stock_in.html'
    form_class = WareHouseTransactionForm

    def get_success_url(self):
        return reverse_lazy(
            'agent:warehouse_detail',
            kwargs={'slug': self.kwargs['slug']}
        )

    def get_success_message(self, transaction):
        return 'Congratulations! You have bought {quantity} {product}.'.format(
            quantity=transaction.quantity,
            product=transaction.product
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        warehouse = WareHouse.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(
            warehouse=warehouse
        )
        kwargs.update({'qs': products})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouse'] = WareHouse.objects.get(slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        transaction = ProductTransaction.objects.create(
            user=self.request.user,
            product=form.cleaned_data['product'],
            transaction_type='I',
            brand=form.cleaned_data['brand'],
            company=form.cleaned_data['company'],
            rate=form.cleaned_data['rate'],
            quantity=form.cleaned_data['quantity'],
            discount=form.cleaned_data['discount'],
        )
        messages.add_message(
            self.request, messages.SUCCESS, self.get_success_message(
                transaction)
        )
        return HttpResponseRedirect(self.get_success_url())


class WareHouseTrasactionStockOut(AgentLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProductTransaction
    template_name = 'agent/warehouse_transaction_stock_out.html'
    fields = []

    def get_success_url(self):
        return reverse_lazy('agent:warehouse_transaction_sell')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouses = AgentProfile.objects.get(
            user=self.request.user).warehouse.all()
        products = Product.objects.filter(
            warehouse__in=warehouses
        )
        context['products'] = products
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        transactions = add_sell_to_transaction(
            request,
            products=request.POST.getlist('product[]'),
            brands=request.POST.getlist('brand[]'),
            companies=request.POST.getlist('company[]'),
            quantity=request.POST.getlist('quantity[]'),
            discounts=request.POST.getlist('discount[]'),
        )
        if transactions:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Congratulations! Product Sales Have Been Recorded',
                extra_tags="success"
            )
        else:
            messages.add_message(
                self.request, messages.ERROR, 'Unable to process request.',
                extra_tags='danger'
            )
        return HttpResponseRedirect(self.get_success_url())


class WareHouseTrasactionSellToZenMembers(AgentLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProductTransaction
    template_name = 'agent/warehouse_transaction_sell_to_zen_members.html'
    fields = []

    def get_success_url(self):
        return reverse_lazy('agent:warehouse_transaction_sell_to_members')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouses = AgentProfile.objects.get(
            user=self.request.user).warehouse.all()
        products = Product.objects.filter(
            warehouse__in=warehouses
        )
        context['members'] = get_user_model().objects.filter(
            ~Q(user_type=STAFF),
            ~Q(pk=self.request.user.pk)
        )
        context['products'] = products
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(
            phone_number=request.POST.get('user', None)
        )
        if user == self.request.user or user.user_type == STAFF:
            messages.add_message(
                self.request, messages.ERROR, 'Unable to process request.',
                extra_tags='danger'
            )
            return HttpResponseRedirect(self.get_success_url())
        transactions = add_sell_to_transaction(
            request,
            products=request.POST.getlist('product[]'),
            brands=request.POST.getlist('brand[]'),
            companies=request.POST.getlist('company[]'),
            quantity=request.POST.getlist('quantity[]'),
            discounts=request.POST.getlist('discount[]'),
            is_member=user
        )
        if transactions:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Congratulations! Product Sales Have Been Recorded',
                extra_tags="success"
            )
        else:
            messages.add_message(
                self.request, messages.ERROR, 'Unable to process request.',
                extra_tags='danger'
            )
        return HttpResponseRedirect(self.get_success_url())


def add_sell_to_transaction(
        request, products, brands, companies, quantity,
        discounts, is_member=None):
    successful_transactions = []
    try:
        for i in range(len(products)):
            product = Product.objects.get(pk=products[i])
            brand = MedicineBrand.objects.get(pk=brands[i])
            company = MedicineCompany.objects.get(pk=companies[i])
            latest_transaction = ProductTransaction.objects.filter(
                product=product,
                brand=brand,
                company=company,
                user=request.user
            ).order_by('-id')[0]
            stocks = calculate_quantity(
                request.user, product, brand, company
            )
            current_quantity = stocks['stock_in'] - stocks['stock_out']
            requested_quantity = int(quantity[i])
            try:
                discount = discounts[i]
            except IndexError:
                discount = 0
            if current_quantity >= requested_quantity:
                transaction_id = ProductTransaction.objects.create(
                    product=product,
                    brand=brand,
                    transaction_type='O',
                    company=company,
                    user=request.user,
                    rate=latest_transaction.rate,
                    quantity=requested_quantity,
                    discount=discount
                )
                if is_member:
                    ProductTransaction.objects.create(
                        product=product,
                        brand=brand,
                        transaction_type='I',
                        company=company,
                        user=is_member,
                        rate=latest_transaction.rate,
                        quantity=requested_quantity,
                        discount=discount
                    )
                successful_transactions.append(transaction_id.pk)
            else:
                ProductTransaction.objects.filter(
                    pk__in=successful_transactions
                ).delete()
                return False
        return successful_transactions
    except Exception:
        return False


def get_product_brands_company(request):
    # requires recode and  query changes/optimizing
    product = request.POST.get('product')
    if product:
        brands = ProductTransaction.objects.filter(
            user=request.user,
            product=product
        ).select_related('brand').values_list('brand', flat=True).distinct()
        company = ProductTransaction.objects.filter(
            user=request.user,
            product=product
        ).select_related('company').values_list('company', flat=True).distinct()
        brands = list(MedicineBrand.objects.filter(
            pk__in=brands
        ).values_list('name', 'pk'))
        company = list(MedicineCompany.objects.filter(
            pk__in=company
        ).values_list('name', 'pk'))
        return JsonResponse(
            {'brands': brands, 'company': company}, safe=False, status=200
        )
    return JsonResponse(
        {'message': 'Brands donot exist.'}, safe=False, status=404
    )


def get_product_rate_via_brand_company(request):
    product = request.POST.get('product')
    brand = request.POST.get('brand')
    company = request.POST.get('company')
    if product and brand and company:
        try:
            rate = ProductTransaction.objects.filter(
                user=request.user,
                product=product,
                brand=brand,
                company=company
            ).order_by('-id')
            if rate:
                return JsonResponse(
                    {'rate': rate[0].rate}, safe=False, status=200
                )
        except ProductTransaction.DoesNotExist:
            pass
    return JsonResponse(
        {'message': 'Not available.'}, safe=False, status=404
    )


def calculate_quantity(user, product, brand, company):
    transactions = ProductTransaction.objects.filter(
        user=user,
        product=product,
        brand=brand,
        company=company
    ).order_by('-id')
    if transactions:
        stock_in = transactions.filter(
            transaction_type='I'
        ).aggregate(Sum('quantity'))['quantity__sum']
        stock_out = transactions.filter(
            transaction_type='O'
        ).aggregate(Sum('quantity'))['quantity__sum']
        return {
            'stock_in': stock_in if stock_in else 0,
            'stock_out': stock_out if stock_out else 0
        }
    return False


def get_product_quantity(request):
    # requires recode and  query changes/optimizing
    product = request.POST.get('product')
    brand = request.POST.get('brand')
    company = request.POST.get('company')
    quantity = int(request.POST.get('quantity'))
    if product and brand and company and quantity:
        stocks = calculate_quantity(request.user, product, brand, company)
        if not stocks:
            return JsonResponse(
                {'message': 'Not available.'}, safe=False, status=404
            )
        current_quantity = stocks['stock_in'] - stocks['stock_out']
        if current_quantity >= quantity:
            status = 'success'
            remaining = current_quantity - quantity
            message = 'You will have '\
                + str(remaining) + ' left in stock'
        else:
            status = 'failure'
            message = 'You currently only have '\
                + str(current_quantity)+' in stock'
        return JsonResponse(
            {
                'quantity': current_quantity,
                'status': status,
                'message': message
            }, safe=False, status=200
        )
    return JsonResponse(
        {'message': 'Not available.'}, safe=False, status=404
    )


class ListDoctors(AgentLoginRequiredMixin, ListView):
    model = DoctorProfile
    template_name = 'agent/doctor/list.html'
    context_object_name = 'doctors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = SubDiscipline.objects.filter(status='A')
        return context

    def get_queryset(self):
        warehouses = AgentProfile.objects.get(
            user=self.request.user
        ).warehouse.all().values_list('discipline_id', flat=True)
        qs = DoctorProfile.objects.filter(
            discipline__in=list(warehouses)
        )
        if self.request.GET.get('first_name'):
            qs = qs.filter(first_name__icontains=self.request.GET.get('first_name'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(last_name__icontains=self.request.GET.get('last_name'))
        if self.request.GET.get('discipline'):
            qs = qs.filter(discipline__pk=self.request.GET.get('discipline'))
        paginator = Paginator(qs, 20)
        page = self.request.GET.get('page')
        qs = paginator.get_page(page)
        return qs


class DoctorDetail(AgentLoginRequiredMixin, DetailView):
    model = DoctorProfile
    template_name = 'agent/doctor/detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        context['organizations'] = Organization.objects.all()
        context['schedules'] = DoctorVistingSchedules.objects.filter(
            doctor=doctor
        ).order_by('-date')
        return context


class ListPatients(AgentLoginRequiredMixin, ListView):
    model = PatientProfile
    template_name = 'agent/patient/list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        return PatientProfile.objects.filter(
            registered_by=self.request.user
        ).order_by('-id')


class CreatePatient(AgentLoginRequiredMixin, FormView):
    template_name = 'agent/patient/form.html'
    form_class = PatientRegistrationForm
    success_url = reverse_lazy('agent:list_patients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provinces'] = Province.objects.all()
        return context

    def form_valid(self, form):
        with transaction.atomic():
            user = get_user_model().objects.create(
                phone_number=form.cleaned_data['phone_number'],
                user_type=PATIENT
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            location = Location.objects.get(
                pk=self.request.POST.get('location', None)
            )
            PatientProfile.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                middle_name=form.cleaned_data['middle_name'],
                designation=form.cleaned_data['designation'],
                permanent_address=location,
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                user=user,
                registered_by=self.request.user
            )
        messages.add_message(
            self.request, messages.SUCCESS,
            'Successfully created new patient. Please enter additional profile details.'
        )
        return HttpResponseRedirect(self.get_success_url())


class UpdatePatient(AgentLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PatientProfile
    template_name = 'agent/patient/update_form.html'
    success_url = reverse_lazy('agent:list_patients')
    success_message = 'Patient profile updated.'
    fields = [
        'first_name', 'last_name', 'middle_name',
        'designation', 'gender', 'permanent_address', 'profile_pic',
        'remark', 'date_of_birth'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provinces'] = Province.objects.all()
        patient = PatientProfile.objects.get(pk=self.kwargs['pk'])
        context['patient'] = patient
        context['zones'] = Zone.objects.filter(
            province=patient.permanent_address.district.zone.province
        )
        context['districts'] = District.objects.filter(
            zone=patient.permanent_address.district.zone
        )
        context['locations'] = Location.objects.filter(
            district=patient.permanent_address.district
        )
        return context


def get_zone_via_province(request):
    try:
        province = Province.objects.get(
            pk=request.POST.get('province')
        )
        zones = Zone.objects.filter(
            province=province
        ).values('id', 'name')
        return JsonResponse(
            {'zones': list(zones)},
            safe=False, status=200
        )
    except Province.DoesNotExist:
        return JsonResponse(
            {'message': 'Not available.'}, safe=False, status=404
        )


def get_district_via_zone(request):
    try:
        zone = Zone.objects.get(
            pk=request.POST.get('zone')
        )
        districts = District.objects.filter(
            zone=zone
        ).values('id', 'name')
        return JsonResponse(
            {'districts': list(districts)},
            safe=False, status=200
        )
    except Province.DoesNotExist:
        return JsonResponse(
            {'message': 'Not available.'}, safe=False, status=404
        )


def get_location_via_district(request):
    try:
        district = District.objects.get(
            pk=request.POST.get('district')
        )
        locations = Location.objects.filter(
            district=district
        ).values('id', 'name')
        return JsonResponse(
            {'locations': list(locations)},
            safe=False, status=200
        )
    except Province.DoesNotExist:
        return JsonResponse(
            {'message': 'Not available.'}, safe=False, status=404
        )


class PatientConsellingFormList(AgentLoginRequiredMixin, ListView):
    model = PatientConsellingQuestionResult
    context_object_name = 'sets'
    template_name = 'agent/counselling/list.html'

    def get_queryset(self):
        patient = PatientProfile.objects.get(pk=self.kwargs['pk'])
        if patient.registered_by == self.request.user:
            return PatientConsellingQuestionResult.objects.filter(
                patient=self.kwargs['pk']
            )
        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientProfile.objects.get(
            pk=self.kwargs['pk']
        )
        return context


class PatientConsellingQuestion(AgentLoginRequiredMixin, FormView):
    form_class = PatientConsellingQuestionForm
    template_name = 'agent/counselling/patient_counselling_form.html'
    success_message = 'Counselling Form Information Saved.'

    def get(self, request, *args, **kwargs):
        self._check_patient_registered_by_agent()
        result = PatientConsellingQuestionResult.objects.get(
            pk=self.kwargs['pk']
        )
        if result.approval_status == 'A':
            messages.add_message(
                self.request, messages.ERROR,
                'Invalid Request.'
            )
            return HttpResponseRedirect(reverse_lazy('agent:list_patients'))
        return self.render_to_response(self.get_context_data())

    def _check_patient_registered_by_agent(self):
        patient = self._get_patient()
        if patient.registered_by != self.request.user:
            raise Http404

    def _get_patient(self):
        return PatientConsellingQuestionResult.objects.get(
            pk=self.kwargs['pk']
        ).patient

    def get_success_url(self):
        patient = self._get_patient()
        return reverse_lazy(
            'agent:patient_counselling_list',
            kwargs={'pk': patient.pk}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['counselling_id'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self._get_patient()
        return context

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR,
            'Please Fill The Form Properly With Available Values.'
        )
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self._check_patient_registered_by_agent()
        with transaction.atomic():
            con_result = PatientConsellingQuestionResult.objects.get(
                pk=self.kwargs['pk']
            )
            con_result.result.clear()
            for field in form:
                question = Question.objects.filter(
                    question=field.name
                )
                if question:
                    question = question[0]
                    set_answer = ConsellingQuestionSetsAnswers.objects.create(
                        question=question
                    )
                    if question.question_type == 'D':
                        set_answer.answer_description = field.value()
                    elif question.question_type == 'O':
                        choice = QuestionChoices.objects.get(
                            pk=field.value()
                        )
                        set_answer.answer_choice = choice
                    set_answer.save()
                    con_result.result.add(set_answer)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Counselling Information Form Saved.'
        )
        return HttpResponseRedirect(self.get_success_url())


class CreatePatientCounselling(AgentLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PatientConsellingQuestionResult
    template_name = 'agent/counselling/question_set.html'
    success_message = 'New Counselling Session Initiated.'
    fields = ['question_set']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientProfile.objects.get(
            pk=self.kwargs['pk']
        )
        return context

    def form_valid(self, form):
        question_set = form.cleaned_data['question_set']
        patient = PatientProfile.objects.get(pk=self.kwargs['pk'])
        if(patient.registered_by != self.request.user):
            messages.add_message(
                self.request, messages.ERROR,
                'Invalid Request.'
            )
            return HttpResponseRedirect(reverse_lazy('agent:list_patients'))
        PatientConsellingQuestionResult.objects.create(
            patient=patient,
            question_set=question_set
        )
        messages.add_message(
            self.request, messages.SUCCESS,
            'Counselling Session Initiated.'
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'agent:patient_counselling_list',
            kwargs={'pk': self.kwargs['pk']}
        )


class ApprovePatientConsellingForm(AgentLoginRequiredMixin, UpdateView):
    model = PatientConsellingQuestionResult
    fields = ['remarks']
    template_name = 'agent/counselling/approve_form.html'

    def get_success_url(self, patient_id):
        return HttpResponseRedirect(reverse_lazy(
            'agent:patient_counselling_list',
            kwargs={'pk': patient_id}
        ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientConsellingQuestionResult.objects.get(
            pk=self.kwargs['pk']
        ).patient
        context['doctors'] = DoctorProfile.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        result = PatientConsellingQuestionResult.objects.get(
            pk=self.kwargs['pk']
        )
        self.object = result
        if result.patient.registered_by != self.request.user:
            messages.add_message(
                self.request, messages.ERROR,
                'Invalid Request.'
            )
            return HttpResponseRedirect(reverse_lazy('agent:list_patients'))
        if result.approval_status == 'A':
            messages.add_message(
                self.request, messages.ERROR,
                'Couselling form has already been approved.'
            )
            return HttpResponseRedirect(reverse_lazy(
                'agent:patient_counselling_list',
                kwargs={'pk': result.patient.pk}
            ))
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        result = PatientConsellingQuestionResult.objects.get(pk=self.kwargs['pk'])
        if result.approval_status == 'A':
            messages.add_message(self.request, messages.ERROR, 'Counselling form has already been approved.')
            return HttpResponseRedirect(reverse_lazy(
                'agent:patient_counselling_list',
                kwargs={'pk': result.patient.pk}
            ))
        if result.patient.registered_by != self.request.user:
            messages.add_message(
                self.request, messages.ERROR,
                'Invalid Request.'
            )
            return HttpResponseRedirect(reverse_lazy('agent:list_patients'))
        if result.question_set.question.count() != result.result.count():
            messages.add_message(
                self.request, messages.ERROR,
                'Counselling form is not complete yet. Please answer all \
                    question in the form before approving it.'
            )
            return HttpResponseRedirect(reverse_lazy(
                'agent:patient_counselling',
                kwargs={'pk': self.kwargs['pk']}
            ))
        appointment = DoctorVistingSchedules.objects.get(pk=self.request.POST.get('appointment'))
        if appointment.date < datetime.date.today():
            messages.add_message(
                self.request, messages.ERROR,
                'Please Select Proper Appointment Date'
            )
            return HttpResponseRedirect(reverse_lazy(
                'agent:patient_counselling',
                kwargs={'pk': self.kwargs['pk']}
            ))
        result.approval_status = 'A'
        result.approved_date = datetime.datetime.now()
        result.approved_by = self.request.user
        result.appointment = appointment
        result.approved_by = self.request.user
        result.remarks = form.cleaned_data['remarks']
        result.save()
        messages.add_message(self.request, messages.SUCCESS, 'Counselling form approved.')
        return self.get_success_url(result.patient.pk)


def get_doctor_appointment(request):
    if request.POST.get('doctor'):
        doctor = DoctorProfile.objects.get(pk=request.POST.get('doctor'))
        schedules = DoctorVistingSchedules.objects.filter(
            doctor=doctor,
            date__gte=datetime.date.today()
        ).values('id', 'in_time', 'out_time', 'organization__name')
        return JsonResponse(
            {'schedules': list(schedules)},
            safe=False, status=200
        )


class PatientConsellingFormView(AgentLoginRequiredMixin, FormView):
    form_class = PatientConsellingQuestionForm
    template_name = 'agent/counselling/patient_counselling_form.html'

    def get(self, request, *args, **kwargs):
        self._check_patient_registered_by_agent()
        return self.render_to_response(self.get_context_data())

    def _check_patient_registered_by_agent(self):
        patient = self._get_patient()
        if patient.registered_by != self.request.user:
            raise Http404

    def _get_patient(self):
        return PatientConsellingQuestionResult.objects.get(
            pk=self.kwargs['pk']
        ).patient

    def get_success_url(self):
        patient = self._get_patient()
        return reverse_lazy(
            'agent:patient_counselling_list',
            kwargs={'pk': patient.pk}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['counselling_id'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self._get_patient()
        context['view_only'] = True
        return context


class LabTest(AgentLoginRequiredMixin, ListView):
    model = PatientLabTest
    template_name = 'agent/lab/patient_test_list.html'
    context_object_name = 'tests'

    def _get_patient(self):
        return PatientProfile.objects.get(pk=self.kwargs['pk'])

    def _check_patient_registered_by_agent(self):
        patient = self._get_patient()
        if patient.registered_by != self.request.user:
            raise Http404

    def get_queryset(self):
        self._check_patient_registered_by_agent()
        return PatientLabTest.objects.filter(
            patient=self._get_patient(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self._get_patient()
        return context


def get_tests_via_lab(request):
    try:
        lab = Labs.objects.get(
            pk=request.POST.get('lab')
        )
        tests = lab.tests.values('id', 'name', 'home_service')
        return JsonResponse(
            {'tests': list(tests)},
            safe=False, status=200
        )
    except Labs.DoesNotExist:
        return JsonResponse(
            {'message': 'Not available.'}, safe=False, status=404
        )


class CreatePatientLabTest(AgentLoginRequiredMixin, CreateView):
    model = PatientLabTest
    template_name = 'agent/lab/patient_test_form.html'
    fields = ['lab', 'requested_date']

    def _get_patient(self):
        return PatientProfile.objects.get(pk=self.kwargs['pk'])

    def _check_patient_registered_by_agent(self):
        patient = self._get_patient()
        if patient.registered_by != self.request.user:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self._get_patient()
        context['provinces'] = Province.objects.all()
        return context

    def _back(self):
        return HttpResponseRedirect(reverse_lazy(
            'agent:patient_lab_add',
            kwargs={'pk': self.kwargs['pk']}
        ))

    def form_valid(self, form):
        deliver_required = self.request.POST.get('delivery_required', 'off')
        delivery_not_required = self.request.POST.get('delivery_not_required', 'off')
        location = None
        home_service = False
        if deliver_required == 'on':
            home_service = True
            location = Location.objects.get(pk=self.request.POST.get('location'))
        if not self.request.POST.get('test'):
            messages.add_message(self.request, messages.ERROR, 'Please select lab first and then test.')
            return self._back()
        if deliver_required not in ('on', 'off') or delivery_not_required not in ('on', 'off'):
            messages.add_message(self.request, messages.ERROR, 'Please select home servive option.')
        try:
            test = LabTests.objects.get(pk=self.request.POST.get('test'))
            lab = form.cleaned_data['lab']
            if test.pk not in list(lab.tests.values_list('id', flat=True)):
                messages.add_message(self.request, messages.ERROR, 'Please select lab first and then test.')
                return self._back()
            PatientLabTest.objects.create(
                patient=PatientProfile.objects.get(pk=self.kwargs['pk']),
                lab=lab,
                test=test,
                location=location,
                home_service=home_service,
                address_detail=self.request.POST.get('address_detail', None),
                requested_date=form.cleaned_data['requested_date'],
                assigned_by=self.request.user,
                delivery_code=uuid.uuid4().hex[:6].upper()
            )
            messages.add_message(self.request, messages.SUCCESS, 'Lab test successfully scheduled.')
            return HttpResponseRedirect(reverse_lazy(
                'agent:patient_lab_list',
                kwargs={'pk': self.kwargs['pk']}
            ))
        except Exception as e:
            print(e)
            messages.add_message(self.request, messages.ERROR, 'Something went wrong. Please fill the form properly and completely.')
            return self._back()
