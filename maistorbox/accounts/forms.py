from django import forms
from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple, ClearableFileInput

from maistorbox.accounts.choices import UserTypeChoice, ContractorRegions, ContractorSpecializations
from maistorbox.accounts.models import ContractorUser, Specializations, Regions, BaseUserModel, ProjectImage
from maistorbox.mixins import FormsStylingMixin


class ContractorUserRegistrationForm(forms.ModelForm, FormsStylingMixin):
    class Meta:
        model = ContractorUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'profile_picture']

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    projects_of_contractor_in_images = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}))

    regions = forms.ModelMultipleChoiceField(
        queryset=Regions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specializations.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        # Create the ContractorUser instance without saving it immediately
        contractor = super().save(commit=False)
        contractor.set_password(self.cleaned_data['password'])  # Set hashed password
        contractor.user_type = UserTypeChoice.CONTRACTOR_USER

        if commit:
            contractor.save()  # Save the user to get a primary key

            # Set many-to-many fields with the related choices
            contractor.specializations.set(self.cleaned_data['specializations'])
            contractor.regions.set(self.cleaned_data['regions'])

        return contractor




class RegularUserRegistrationForm(forms.ModelForm, FormsStylingMixin):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'confirm_password']

    def save(self, commit=True):
        User = get_user_model()
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.user_type = UserTypeChoice.REGULAR_USER

        if commit:
            user.save()

            return user

        return user

