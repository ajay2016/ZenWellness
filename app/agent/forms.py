from django import forms
from warehouse.models import ProductTransaction
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from core.models import Designation
from healthcare.models import PatientConsellingQuestionResult, PatientProfile

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class WareHouseTransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super(WareHouseTransactionForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = qs

    class Meta:
        model = ProductTransaction
        fields = ['product', 'brand', 'company', 'rate', 'quantity', 'discount']


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
    date_of_birth = forms.DateField()
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
