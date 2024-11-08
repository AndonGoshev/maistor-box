from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from maistorbox.accounts.choices import UserTypeChoice
from maistorbox.accounts.models import BaseUserModel, ContractorUserModel, Regions, Specializations
from maistorbox.mixins import FormsStylingMixin


class BaseUserRegistrationForm(UserCreationForm, FormsStylingMixin):
    class Meta:
        model = BaseUserModel
        fields = ('username', 'email', 'password1', 'password2')


class ContractorUserRegistrationForm(UserCreationForm, FormsStylingMixin):
    # Base user fields
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        required=True,
        max_length=50,
    )
    last_name = forms.CharField(
        required=True,
        max_length=50,
    )


    # Contractor user fields
    phone_number = forms.CharField(
        required=True,
        max_length=20,
    )
    profile_image = forms.ImageField(
        required=True,
    )
    regions = forms.ModelMultipleChoiceField(
        queryset=Regions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specializations.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = BaseUserModel
        fields = ['username', 'password1', 'password2', 'email',]


    def save(self, commit=True):

        # Here we are saving the base part of the contractor user
        base_user = super().save(commit=False)
        base_user.first_name = self.cleaned_data['first_name']
        base_user.last_name = self.cleaned_data['last_name']
        base_user.email = self.cleaned_data['email']
        base_user.user_type = UserTypeChoice.CONTRACTOR_USER

        if commit:
            base_user.save()

        # Here we are saving the additional part for the contractor user
        contractor_user = ContractorUserModel(
            user=base_user,
            phone_number=self.cleaned_data['phone_number'],
            profile_image=self.cleaned_data.get('profile_image'),
        )

        if commit:
            contractor_user.save()
            contractor_user.regions.set(self.cleaned_data['regions'])
            contractor_user.specializations.set(self.cleaned_data['specializations'])

        return base_user


class CustomLoginForm(AuthenticationForm, FormsStylingMixin):
    pass