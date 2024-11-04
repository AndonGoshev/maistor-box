from django import forms
from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple

from maistorbox.accounts.choices import UserTypeChoice
from maistorbox.accounts.models import ContractorUser, Specializations, Regions, BaseUserModel, ProjectImage


class ContractorUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Masked password input
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ContractorUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password', 'profile_picture', 'specializations', 'regions']


    specializations = forms.ModelMultipleChoiceField(
        queryset=Specializations.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    regions = forms.ModelMultipleChoiceField(
        queryset=Regions.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=False):
        User = get_user_model()
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.user_type = UserTypeChoice.CONTRACTOR_USER

        if commit:
            user.save()
            contractor = ContractorUser.objects.create_user(
                user=user,
                profile_picture=self.cleaned_data['profile_picture']
            )

            contractor.specializations.set(self.cleaned_data['specializations'])
            contractor.regions.set(self.cleaned_data['regions'])
            contractor.save()

            project_images = self.cleaned_data['project_images']
            if project_images:
                for image in project_images:
                    ProjectImage.objects.create(contractor=contractor, image=image)

            return contractor


        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "username":
                self.fields[field].help_text = 'Полето може да съдържа само букви цифри и (@ . + - _)'
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = field




class RegularUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        User = get_user_model()
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['emails'])
        user.set_password(self.cleaned_data['password'])
        user_type = UserTypeChoice.REGULAR_USER

        if commit:
            user.save()

            return user

        return user

