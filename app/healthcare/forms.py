from datetime import date
from django import forms
from core.models import Designation
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from core.models import University, Degree, SubDiscipline
from .models import (
    DoctorProfile, PatientProfile, PatientConsellingQuestionResult,
    DoctorVistingSchedules, Labs, LabAgentProfile
)


ACTIVE = 'A'
INACTIVE = 'I'
STATUS = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive'),
)

CHOICES = (
    ('', '-----------'),
)
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class DoctorRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    middle_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255)
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all()
    )
    discipline = forms.ModelChoiceField(
        queryset=SubDiscipline.objects.all()
    )
    status = forms.ChoiceField(
        choices=STATUS
    )
    phone_number = forms.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)]
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )
    remark = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'User with phone number exists.')
        for char in phone_number:
            if not char.isdigit():
                self.add_error('phone_number', 'Please Only Enter Numeric Digits.')


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            'first_name', 'last_name', 'middle_name', 'discipline',
            'designation', 'permanent_address', 'profile_pic',
            'remark'
        ]


class DoctorPasswordChangeForm(forms.Form):
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )


class DoctorDegreeForm(forms.Form):
    degree = forms.ModelChoiceField(
        queryset=Degree.objects.filter(status=ACTIVE)
    )
    university = forms.CharField(
        max_length=255,
    )

    def clean(self):
        cleaned_data = super().clean()
        university = None
        if cleaned_data.get("university"):
            university = int(cleaned_data.get("university"))
        if not University.objects.filter(pk=university).exists():
            self.add_error('university', 'Please Select Valid University.')
        assc_uni = list(cleaned_data.get('degree').university.all().values_list(
            'pk', flat=True))
        if university not in assc_uni:
            self.add_error('university', 'Please Select Valid Degree and University.')
        cleaned_data['university'] = University.objects.get(pk=university)


class PatientRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    middle_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255)
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all()
    )
    gender = forms.ChoiceField(
        choices=GENDER
    )
    phone_number = forms.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)]
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'User with phone number exists.')
        for char in phone_number:
            if not char.isdigit():
                self.add_error('phone_number', 'Please Only Enter Numeric Digits.')


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'first_name', 'last_name', 'middle_name',
            'designation', 'gender', 'approval_status', 'permanent_address',
            'profile_pic', 'remark', 'date_of_birth'
        ]


class PatientConsellingQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        counselling_set = PatientConsellingQuestionResult.objects.get(
            pk=kwargs.pop('counselling_id')
        )
        super(PatientConsellingQuestionForm, self).__init__(*args, **kwargs)
        results = counselling_set.result
        questions = counselling_set.question_set.question.all()
        for question in questions:
            current_answer = results.filter(
                question=question
            )
            if question.question_type == 'O':
                options = []
                for choice in question.question_choices.all():
                    options.append((choice.pk, choice.name))
                self.fields[question.question] = forms.ChoiceField(
                    choices=options
                )
            elif question.question_type == 'D':
                self.fields[question.question] = forms.CharField(
                    widget=forms.Textarea
                )

            if current_answer:
                field = self.fields[question.question]
                if question.question_type == 'O':
                    field.initial = current_answer[0].answer_choice.pk
                elif question.question_type == 'D':
                    field.initial = current_answer[0].answer_description


class DoctorVistingScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorVistingSchedules
        fields = ('date', 'in_time', 'out_time', 'organization', 'remark')

    def clean(self):
        cleaned_data = super().clean()
        schedule_date = cleaned_data.get("date")
        if schedule_date < date.today():
            self.add_error('date', 'Please Select Proper Date.')
        if cleaned_data.get("in_time") > cleaned_data.get("out_time"):
            self.add_error('out_time', 'Please Select Proper Out Time.')


class LabAgentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    middle_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255)
    lab = forms.ModelChoiceField(
        queryset=Labs.objects.all()
    )
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all()
    )
    gender = forms.ChoiceField(
        choices=GENDER
    )
    phone_number = forms.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)]
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'User with phone number exists.')
        for char in phone_number:
            if not char.isdigit():
                self.add_error('phone_number', 'Please Only Enter Numeric Digits.')


class LabAgentProfileForm(forms.ModelForm):
    class Meta:
        model = LabAgentProfile
        fields = [
            'first_name', 'last_name', 'middle_name', 'lab',
            'designation', 'gender', 'status', 'permanent_address',
            'profile_pic', 'remark', 'date_of_birth'
        ]
