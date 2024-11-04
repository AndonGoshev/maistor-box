from django import forms
from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple

from maistorbox.accounts.choices import UserTypeChoice
from maistorbox.accounts.models import ContractorUser, Specializations, Regions, BaseUserModel, ProjectImage


class ContractorUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = ContractorUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name','profile_picture', 'specializations', 'regions']

    specializations = forms.ModelMultipleChoiceField(
        queryset=Specializations.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    regions = forms.ModelMultipleChoiceField(
        queryset=Regions.objects.all(),
        widget=CheckboxSelectMultiple,
    )

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

