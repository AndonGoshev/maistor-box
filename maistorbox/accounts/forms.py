from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.forms import BaseModelForm, BaseModelFormSet, ClearableFileInput

from maistorbox.accounts.choices import UserTypeChoice
from maistorbox.accounts.models import BaseUserModel, ContractorUserModel, Region, Specialization, ContractorProjectModel, \
    ImageModel
from maistorbox.mixins import FormsStylingMixin, ErrorMessagesTranslateMixin


class CustomClearableFileInput(forms.ClearableFileInput):
    initial_text = ''  # Clear any default "Currently" label
    input_text = ''  # Clear any default "Change" label

class BaseUserRegistrationForm(ErrorMessagesTranslateMixin, UserCreationForm, FormsStylingMixin):
    class Meta:
        model = BaseUserModel
        fields = ('username', 'email', 'password1', 'password2')

    # We are overriding the save method because when the user is added through the admin panel
    # the password is not hashed and this leads to the created user not being able
    # to log in.
    def save(self, commit=True):
        regular_user = super().save(commit=False)
        regular_user.set_password(self.cleaned_data['password1'])

        if commit:
            regular_user.save()

        return regular_user






class ContractorUserRegistrationForm(ErrorMessagesTranslateMixin, UserCreationForm, FormsStylingMixin):
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
        queryset=Region.objects.all(),
        required=True
    )
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        required=True
    )

    class Meta:
        model = BaseUserModel
        fields = ['username', 'password1', 'password2', 'email', ]

    def save(self, commit=True):

        # Here we are saving the base part of the contractor user
        base_user = super().save(commit=False)
        base_user.set_password(self.cleaned_data['password1'])
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


class ContractorUserProfileEditForm(forms.ModelForm,  FormsStylingMixin, ErrorMessagesTranslateMixin):
    # Include fields from the related BaseUserModel (first_name, last_name)
    first_name = forms.CharField(
        max_length=50,
        required=True,
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
    )

    # Fields from ContractorUserModel
    class Meta:
        model = ContractorUserModel
        fields = ['about_me', 'phone_number', 'profile_image', 'regions', 'specializations']
        widgets = {
            'profile_image': CustomClearableFileInput()
        }

    # Add additional logic to ensure first_name, last_name are properly populated
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the first_name and last_name from the related BaseUserModel instance
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        # Save the related BaseUserModel fields (first_name, last_name)
        base_user = self.instance.user
        base_user.first_name = self.cleaned_data['first_name']
        base_user.last_name = self.cleaned_data['last_name']
        if commit:
            base_user.save()

        # Now save the contractor user model fields (about_me, phone_number, etc.)
        contractor_user = super().save(commit)

        return contractor_user

class ContractorProjectCreateForm(forms.ModelForm, FormsStylingMixin, ):
    class Meta:
        model = ContractorProjectModel
        exclude = ['contractor_user', ]


class ContractorProjectEditForm(forms.ModelForm, FormsStylingMixin, ):
    class Meta:
        model = ContractorProjectModel
        exclude = ['contractor_user', ]


class ImageForm(forms.ModelForm, FormsStylingMixin):
    class Meta:
        model = ImageModel
        exclude = ['contractor_project', ]
        widgets = {
            'image': CustomClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically set the button label based on whether the image exists
        if self.instance.image:
            self.fields['image'].widget.attrs['class'] = 'change-image'  # Add your own class
            self.fields['image'].label = "Смени"
        else:
            self.fields['image'].widget.attrs['class'] = 'upload-image'  # Add your own class
            self.fields['image'].label = "Качи снимка"


class CustomImageFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        queryset = kwargs.get('queryset', None)
        extra_images_needed = 8
        if queryset:
            extra_images_needed = 8 - queryset.count()

        kwargs['extra'] = max(0, extra_images_needed)

        super().__init__(*args, **kwargs)


CreateImageFormSet = forms.modelformset_factory(
    ImageModel,
    form=ImageForm,
    extra=8,
)

EditImageFormSet = forms.modelformset_factory(
    ImageModel,
    form=ImageForm,
    formset=CustomImageFormSet,
)


class CustomLoginForm(AuthenticationForm, FormsStylingMixin):
    pass


class CustomPasswordChangeForm(PasswordChangeForm, FormsStylingMixin):
    pass


class CustomPasswordResetForm(PasswordResetForm, FormsStylingMixin):
    pass


class CustomPasswordSetForm(SetPasswordForm, FormsStylingMixin):
    pass
