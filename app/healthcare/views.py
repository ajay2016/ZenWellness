from django.views.generic import (
    ListView, FormView, UpdateView, DeleteView, CreateView,
    DetailView
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from website.mixins import CheckAdminUserMixin
from core.constants import (
    DOCTOR, PATIENT, LAB
)
from .forms import (
    DoctorRegistrationForm, DoctorProfileForm,
    DoctorDegreeForm, DoctorPasswordChangeForm,
    PatientRegistrationForm, PatientProfileForm,
    PatientConsellingQuestionForm, DoctorVistingScheduleForm,
    LabAgentRegistrationForm, LabAgentProfileForm
)
from .models import (
    DoctorProfile, DoctorDegree, Question, ConsellingQuestionSets,
    PatientConsellingQuestionResult, PatientProfile, QuestionChoices,
    ConsellingQuestionSetsAnswers, Organization, DoctorVistingSchedules,
    LabTestItems, LabTests, Labs, LabAgentProfile
)
from django.db.utils import IntegrityError


class DoctorList(CheckAdminUserMixin, ListView):
    model = DoctorProfile
    template_name = 'healthcare/doctor/doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        return DoctorProfile.objects.select_related('user').all()


class DoctorCreate(CheckAdminUserMixin, SuccessMessageMixin, FormView):
    template_name = 'healthcare/doctor/doctor_form.html'
    form_class = DoctorRegistrationForm

    def form_valid(self, form):
        with transaction.atomic():
            user = get_user_model().objects.create_user(
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],
                user_type=DOCTOR,
            )
            profile = DoctorProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                designation=form.cleaned_data['designation'],
                discipline=form.cleaned_data['discipline'],
            )
        return HttpResponseRedirect(reverse_lazy(
            'healthcare:doctor_profile_update',
            kwargs={'pk': profile.pk}
        ))


class DoctorProfileView(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = DoctorProfile
    template_name = 'healthcare/doctor/doctor_profile.html'
    form_class = DoctorProfileForm
    context_object_name = 'profile'
    success_message = 'Profile Updated.'

    def get_success_url(self):
        return reverse_lazy(
            'healthcare:doctor_profile_update',
            kwargs={'pk': self.kwargs['pk']}
        )


class DoctorDegreeList(CheckAdminUserMixin, SuccessMessageMixin, ListView):
    model = DoctorDegree
    template_name = 'healthcare/doctor/doctor_degree_list.html'
    context_object_name = 'degrees'

    def get_context_data(self, **kwargs):
        context = super(DoctorDegreeList, self).get_context_data(**kwargs)
        context['doctor'] = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return DoctorDegree.objects.filter(doctor=self.kwargs['pk'])


class DoctorDegreeCreate(CheckAdminUserMixin, SuccessMessageMixin, FormView):
    template_name = 'healthcare/doctor/doctor_degree_form.html'
    form_class = DoctorDegreeForm
    success_message = "A New Degree Has Been Added."

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Degree'
        context['form_action'] = reverse_lazy(
            'healthcare:doctor_degree_add',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            'healthcare:doctor_degree_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def form_valid(self, form):
        doctor_profile = DoctorProfile.objects.get(
            pk=self.kwargs['pk']
        )
        try:
            DoctorDegree.objects.create(
                doctor=doctor_profile,
                degree=form.cleaned_data['degree'],
                university=form.cleaned_data['university']
            )
        except IntegrityError:
            messages.add_message(
                self.request, messages.ERROR, 'Data Already Exists.'
            )
            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.get_success_url())


class DoctorDegreeDeleteView(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = DoctorDegree
    success_message = "Doctor's Degree Has Been Removed."

    def get_success_url(self, pk):
        return reverse_lazy(
            'healthcare:doctor_degree_list',
            kwargs={'pk': pk}
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        pk = obj.doctor.pk
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.get_success_url(pk))


class DoctorChangePassword(CheckAdminUserMixin, SuccessMessageMixin, FormView):
    model = get_user_model()
    success_message = "Doctor's Password Has Been Changed."
    template_name = 'healthcare/doctor/doctor_password_form.html'
    form_class = DoctorPasswordChangeForm
    success_url = reverse_lazy('healthcare:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['doctor'] = get_user_model().objects.get(
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
                return HttpResponseRedirect(self.get_success_url(
                    self.kwargs['pk'])
                )
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


class QuestionChoiceList(CheckAdminUserMixin, ListView):
    model = QuestionChoices
    context_object_name = 'choices'
    template_name = 'healthcare/counselling/question_choice.html'


class QuestionChoiceCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = QuestionChoices
    fields = ('name',)
    success_url = reverse_lazy('healthcare:question_choice')
    success_message = "A New Choice Has Been Added."
    template_name = 'healthcare/counselling/question_choice_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Choice'
        context['form_action'] = reverse_lazy('healthcare:question_choice_add')
        return context


class QuestionChoiceUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = QuestionChoices
    fields = ('name',)
    success_url = reverse_lazy('healthcare:question_choice')
    success_message = "Choice Information Has Been Updated."
    slug_field = 'name'
    template_name = 'healthcare/counselling/question_choice_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Update Country' + self.get_object().name
        context['form_action'] = reverse_lazy(
                'healthcare:question_choice_update',
                kwargs={'slug': self.kwargs['slug']}
            )
        return context


class QuestionChoiceDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = QuestionChoices
    success_url = reverse_lazy('healthcare:question_choice')
    success_message = "Choice Has Been Removed."
    slug_field = 'name'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class QuestionList(CheckAdminUserMixin, ListView):
    model = Question
    template_name = 'healthcare/counselling/question_list.html'
    context_object_name = 'questions'


class QuestionCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Question
    fields = ('question', 'question_type', 'question_choices')
    success_url = reverse_lazy('healthcare:question_list')
    success_message = "A New Question Has Been Added."
    template_name = 'healthcare/counselling/question_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Question'
        context['form_action'] = reverse_lazy('healthcare:question_add')
        return context


class QuestionUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Question
    fields = ('question', 'question_type', 'question_choices')
    success_url = reverse_lazy('healthcare:question_list')
    success_message = "Question Has Been Updated."
    template_name = 'healthcare/counselling/question_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Update Question-' + self.get_object().question
        context['form_action'] = reverse_lazy(
                'healthcare:question_update',
                kwargs={'pk': self.kwargs['pk']}
            )
        return context


class QuestionDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('healthcare:question_list')
    success_message = "Question Has Been Removed."

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class CounsellingQuestionSetList(CheckAdminUserMixin, ListView):
    model = ConsellingQuestionSets
    template_name = 'healthcare/counselling/question_sets_list.html'
    context_object_name = 'sets'


class CounsellingQuestionSetCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = ConsellingQuestionSets
    fields = ('name', 'question')
    success_url = reverse_lazy('healthcare:coun_question_set_list')
    success_message = "A New Counselling Question Set Has Been Created."
    template_name = 'healthcare/counselling/question_sets_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Add New Question'
        context['form_action'] = reverse_lazy('healthcare:coun_question_set_add')
        return context


class CounsellingQuestionSetUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = ConsellingQuestionSets
    fields = ('name', 'question')
    success_url = reverse_lazy('healthcare:coun_question_set_list')
    success_message = "Counselling Question Set Has Been Updated."
    template_name = 'healthcare/counselling/question_sets_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_title'] = 'Update Couselling Question Set-' + self.get_object().name
        context['form_action'] = reverse_lazy(
                'healthcare:coun_question_set_update',
                kwargs={'pk': self.kwargs['pk']}
            )
        return context


class CounsellingQuestionSetDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = ConsellingQuestionSets
    success_url = reverse_lazy('healthcare:coun_question_set_list')
    success_message = "Question Has Been Removed."

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class PatientList(CheckAdminUserMixin, ListView):
    model = PatientProfile
    template_name = 'healthcare/patient/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        return PatientProfile.objects.select_related('user').all()


class PatientCreate(CheckAdminUserMixin, SuccessMessageMixin, FormView):
    template_name = 'healthcare/patient/patient_form.html'
    form_class = PatientRegistrationForm

    def form_valid(self, form):
        with transaction.atomic():
            user = get_user_model().objects.create_user(
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],
                user_type=PATIENT,
            )
            profile = PatientProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                designation=form.cleaned_data['designation'],
                gender=form.cleaned_data['gender'],
            )
        return HttpResponseRedirect(reverse_lazy(
            'healthcare:patient_profile_update',
            kwargs={'pk': profile.pk}
        ))


class PatientProfileView(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = PatientProfile
    template_name = 'healthcare/patient/patient_profile.html'
    form_class = PatientProfileForm
    context_object_name = 'profile'
    success_message = 'Profile Updated.'

    def get_success_url(self):
        return reverse_lazy(
            'healthcare:patient_profile_update',
            kwargs={'pk': self.kwargs['pk']}
        )


class PatientConsellingQuestionSets(CheckAdminUserMixin, ListView):
    model = PatientConsellingQuestionResult
    context_object_name = 'sets'
    template_name = 'healthcare/counselling/patient_question_sets.html'

    def get_queryset(self):
        return PatientConsellingQuestionResult.objects.filter(
            patient=self.kwargs['pk']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientProfile.objects.get(
            pk=self.kwargs['pk']
        )
        return context


class PatientConsellingQuestionSetCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = PatientConsellingQuestionResult
    template_name = 'healthcare/counselling/patient_question_sets_form.html'
    fields = ['question_set']
    success_message = 'Patient Has Been Assigned New Counselling Question Set'

    def get_success_url(self):
        return reverse_lazy(
            'healthcare:patient_counselling_question_sets_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientProfile.objects.get(
            pk=self.kwargs['pk']
        )
        return context

    def form_valid(self, form):
        patient = PatientProfile.objects.get(
            pk=self.kwargs['pk']
        )
        PatientConsellingQuestionResult.objects.create(
            question_set=form.cleaned_data['question_set'],
            patient=patient
        )
        return HttpResponseRedirect(self.get_success_url())


class PatientConsellingQuestionForm(CheckAdminUserMixin, SuccessMessageMixin, FormView):
    form_class = PatientConsellingQuestionForm
    template_name = 'healthcare/counselling/patient_counselling_form.html'
    success_message = 'Counselling Form Information Saved.'

    def get_success_url(self):
        coun_set = PatientConsellingQuestionResult.objects.get(
            pk=self.kwargs['pk']
        )
        return reverse_lazy(
            'healthcare:patient_counselling_question_sets_list',
            kwargs={'pk': coun_set.patient.pk}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['counselling_id'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = PatientConsellingQuestionResult.objects.get(
            pk=self.kwargs['pk']
        ).patient
        return context

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR,
            'Please Fill The Form Properly With Available Values.'
        )
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
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


class OrganizationList(CheckAdminUserMixin, ListView):
    model = Organization
    template_name = 'healthcare/organizations/organization_list.html'
    context_object_name = 'organizations'


class OrganizationCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Organization
    fields = ('name', 'location', 'image', 'remark')
    template_name = 'healthcare/organizations/organization_form.html'
    success_url = reverse_lazy('healthcare:organization_list')
    success_message = 'Organization was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Organization'
        context['form_action'] = reverse_lazy('healthcare:organization_add')
        return context


class OrganizationUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Organization
    fields = ('name', 'location', 'image', 'remark')
    template_name = 'healthcare/organizations/organization_form.html'
    success_url = reverse_lazy('healthcare:organization_list')
    success_message = 'Organization was updated successfully'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Organization - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'healthcare:organization_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class OrganizationDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Organization
    http_method_names = ['get']
    success_url = reverse_lazy('healthcare:organization_list')
    success_message = 'Organization was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class DoctorVisitingSchedulesList(CheckAdminUserMixin, ListView):
    model = DoctorVistingSchedules
    template_name = 'healthcare/visiting_schedule/list.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        return DoctorVistingSchedules.objects.filter(doctor=doctor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        return context


class DoctorVisitingSchedulesCreate(CheckAdminUserMixin, CreateView):
    model = DoctorVistingSchedules
    template_name = 'healthcare/visiting_schedule/form.html'
    form_class = DoctorVistingScheduleForm
    success_message = 'New Schedule was created successfully'

    def get_success_url(self):
        return reverse_lazy(
            'healthcare:doctor_schedule_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        context['form_title'] = 'Add New Schedule - ' \
            + doctor.first_name + ' ' + doctor.last_name
        context['form_action'] = reverse_lazy(
            'healthcare:doctor_schedule_add',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context

    def form_valid(self, form):
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        try:
            DoctorVistingSchedules.objects.create(
                doctor=doctor,
                organization=form.cleaned_data['organization'],
                date=form.cleaned_data['date'],
                in_time=form.cleaned_data['in_time'],
                out_time=form.cleaned_data['out_time'],
            )
        except IntegrityError:
            messages.add_message(
                self.request, messages.ERROR, 'Duplicate Entry'
            )
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.get_success_url())


class DoctorVisitingSchedulesUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = DoctorVistingSchedules
    template_name = 'healthcare/visiting_schedule/form.html'
    form_class = DoctorVistingScheduleForm
    success_message = 'Schedule was updated successfully'

    def get_success_url(self):
        return reverse_lazy(
            'healthcare:doctor_schedule_list',
            kwargs={'pk': self.object.doctor.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object.doctor
        print(doctor)
        context['form_title'] = 'Update Schedule - ' \
            + doctor.first_name + ' ' + doctor.last_name
        context['form_action'] = reverse_lazy(
            'healthcare:doctor_schedule_update',
            kwargs={'pk': self.kwargs['pk']}
        )
        return context

    def form_valid(self, form):
        try:
            return super(DoctorVisitingSchedulesUpdate, self).form_valid(form)
        except IntegrityError:
            messages.add_message(
                self.request, messages.ERROR, 'Duplicate Entry'
            )
            return HttpResponseRedirect(self.get_success_url())


class DoctorVisitingSchedulesDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = DoctorVistingSchedules
    http_method_names = ['get']
    success_message = 'Schedule was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        pk = obj.doctor.pk
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(reverse_lazy(
            'healthcare:doctor_schedule_list',
            kwargs={'pk': pk}
        ))


class LabTestItemsList(CheckAdminUserMixin, ListView):
    model = LabTestItems
    template_name = 'healthcare/lab/items_list.html'
    context_object_name = 'items'


class LabTestItemsCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = LabTestItems
    fields = ('name', 'remark')
    template_name = 'healthcare/lab/items_form.html'
    success_url = reverse_lazy('healthcare:lab_test_items_list')
    success_message = 'Lab Test Item was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Lab Test Item'
        context['form_action'] = reverse_lazy('healthcare:lab_test_items_add')
        return context


class LabTestItemsUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = LabTestItems
    fields = ('name', 'remark')
    template_name = 'healthcare/lab/items_form.html'
    success_url = reverse_lazy('healthcare:lab_test_items_list')
    success_message = 'Lab Test Item was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Lab Test Item - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'healthcare:lab_test_items_update',
            kwargs={'pk': self.get_object().pk}
        )
        return context


class LabTestItemsDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = LabTestItems
    http_method_names = ['get']
    success_url = reverse_lazy('healthcare:lab_test_items_list')
    success_message = 'Lab Test Item was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class LabTestsList(CheckAdminUserMixin, ListView):
    model = LabTests
    template_name = 'healthcare/lab/tests_list.html'
    context_object_name = 'tests'


class LabTestsCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = LabTests
    fields = ('name', 'home_service', 'items', 'remark')
    template_name = 'healthcare/lab/tests_form.html'
    success_url = reverse_lazy('healthcare:lab_tests_list')
    success_message = 'Lab Test was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Lab Test'
        context['form_action'] = reverse_lazy('healthcare:lab_tests_add')
        return context


class LabTestsUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = LabTests
    fields = ('name', 'home_service', 'items', 'remark')
    template_name = 'healthcare/lab/tests_form.html'
    success_url = reverse_lazy('healthcare:lab_tests_list')
    success_message = 'Lab Test was updated successfully'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Lab Test - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'healthcare:lab_tests_update',
            kwargs={'slug': self.kwargs['slug']}
        )
        return context


class LabTestsDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = LabTests
    http_method_names = ['get']
    success_url = reverse_lazy('healthcare:lab_tests_list')
    success_message = 'Lab Test was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class LabTestsItems(CheckAdminUserMixin, DetailView):
    model = LabTests
    context_object_name = 'test'
    template_name = 'healthcare/lab/tests_items_list.html'


class LabsList(CheckAdminUserMixin, ListView):
    model = Labs
    template_name = 'healthcare/lab/labs_list.html'
    context_object_name = 'labs'


class LabsCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Labs
    fields = ('name', 'tests', 'location', 'remark')
    template_name = 'healthcare/lab/labs_form.html'
    success_url = reverse_lazy('healthcare:labs_list')
    success_message = 'Lab was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Lab'
        context['form_action'] = reverse_lazy('healthcare:labs_add')
        return context


class LabsUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Labs
    fields = ('name', 'tests', 'location', 'remark')
    template_name = 'healthcare/lab/labs_form.html'
    success_url = reverse_lazy('healthcare:labs_list')
    success_message = 'Lab was updated successfully'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Lab - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'healthcare:labs_update',
            kwargs={'slug': self.kwargs['slug']}
        )
        return context


class LabsDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Labs
    http_method_names = ['get']
    success_url = reverse_lazy('healthcare:labs_list')
    success_message = 'Lab was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class LabsTests(CheckAdminUserMixin, DetailView):
    model = Labs
    context_object_name = 'lab'
    template_name = 'healthcare/lab/lab_tests_list.html'


class LabAgentList(CheckAdminUserMixin, ListView):
    model = LabAgentProfile
    context_object_name = 'lab_agents'
    template_name = 'healthcare/labagent/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab'] = Labs.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        lab = Labs.objects.get(slug=self.kwargs['slug'])
        return LabAgentProfile.objects.filter(
            lab=lab
        )


class LabAgentsCreate(CheckAdminUserMixin, FormView):
    template_name = 'healthcare/labagent/form.html'
    form_class = LabAgentRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab'] = Labs.objects.get(slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        with transaction.atomic():
            user = get_user_model().objects.create_user(
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],
                user_type=LAB,
                is_superuser=True
            )
            lab = Labs.objects.get(slug=self.kwargs['slug'])
            profile = LabAgentProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                designation=form.cleaned_data['designation'],
                gender=form.cleaned_data['gender'],
                lab=lab
            )
        return HttpResponseRedirect(reverse_lazy(
            'healthcare:lab_agents_update',
            kwargs={'pk': profile.pk}
        ))


class LabAgentsProfileUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = LabAgentProfile
    template_name = 'healthcare/labagent/profile.html'
    form_class = LabAgentProfileForm
    context_object_name = 'profile'
    success_message = 'Profile Updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab_agent = LabAgentProfile.objects.get(pk=self.kwargs['pk'])
        context['lab'] = lab_agent.lab
        return context

    def get_success_url(self):
        return reverse_lazy(
            'healthcare:lab_agents_update',
            kwargs={'pk': self.kwargs['pk']}
        )
