from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from django.core.validators import MinLengthValidator
from .models import Designation, Location
from warehouse.models import AgentProfile


class AdminLogin(forms.Form):
    phone_number = forms.IntegerField(
        label=_('phone_number'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('enter_phone_number_login_form')
        })
    )
    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('enter_password_login_form')
        })
    )


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class AgentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    middle_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255)
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all()
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all()
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


class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = [
            'first_name', 'middle_name', 'last_name',
            'location', 'designation', 'permanent_address', 'profile_pic',
            'remark'
        ]


class AgentPasswordChangeForm(forms.Form):
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )


class AgentWarehouseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super(AgentWarehouseForm, self).__init__(*args, **kwargs)
        self.fields['warehouse'].queryset = qs

    class Meta:
        model = AgentProfile
        fields = ['warehouse']
