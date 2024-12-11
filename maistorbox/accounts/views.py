from lib2to3.fixes.fix_input import context

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView, DeleteView, UpdateView
from django.contrib import messages

from maistorbox import settings
from maistorbox.accounts.forms import BaseUserRegistrationForm, ContractorUserRegistrationForm, CustomLoginForm, \
    CustomPasswordChangeForm, CustomPasswordSetForm, CustomPasswordResetForm, ContractorProjectCreateForm, \
    ImageForm, CreateImageFormSet, ContractorUserProfileEditForm
from maistorbox.accounts.models import BaseUserModel, ContractorProjectModel, ImageModel, ContractorUserModel
from maistorbox.mixins import PrivateProfilesViewsPermissionRequiredMixin, CustomLoginRequiredMixin, \
    PrivateContractorProjectsViewsPermissionRequiredMixin


class BaseUserRegistrationView(CreateView):
    form_class = BaseUserRegistrationForm
    template_name = 'accounts/regular-users/regular-user-registration.html'
    success_url = reverse_lazy('login')
    redirect_url = reverse_lazy('regular-user-registration')


class RegularUserProfileView(CustomLoginRequiredMixin, PrivateProfilesViewsPermissionRequiredMixin, TemplateView):
    template_name = 'accounts/regular-users/regular-user-profile-details.html'


class RegularUserProfileDeleteView(CustomLoginRequiredMixin, PrivateProfilesViewsPermissionRequiredMixin, DeleteView):
    model = BaseUserModel
    success_url = reverse_lazy('home_page')
    template_name = 'accounts/common/profile-delete.html'
    pk_url_kwarg = 'id'


class ContractorUserRegistrationView(CreateView):
    form_class = ContractorUserRegistrationForm
    template_name = 'accounts/contractors/contractor-registration.html'
    success_url = reverse_lazy('login')
    redirect_url = reverse_lazy('contractor-registration')



class ContractorUserProfileDetailsView(CustomLoginRequiredMixin, PrivateProfilesViewsPermissionRequiredMixin, TemplateView):
    template_name = 'accounts/contractors/contractor-profile-details.html'


class ContractorUserProfileEditView(CustomLoginRequiredMixin, PrivateProfilesViewsPermissionRequiredMixin, UpdateView):
    model = ContractorUserModel
    form_class = ContractorUserProfileEditForm  # Use the custom form for editing
    template_name = 'accounts/contractors/contractor-profile-edit.html'
    success_url = reverse_lazy('contractor-user-profile-details')  # Change to the desired success URL

    def get_success_url(self):
        contractor_id = self.request.user.id
        return reverse('contractor-user-profile-details', kwargs={'id': contractor_id})

    # This method ensures that we get the current contractor user based on the logged-in user
    def get_object(self, queryset=None):
        return self.request.user.contractor_user





class ContractorProjectCreateView(PrivateProfilesViewsPermissionRequiredMixin, CreateView):
    model = ContractorProjectModel
    form_class = ContractorProjectCreateForm
    template_name = 'accounts/contractors/project-create.html'
    success_url = reverse_lazy('contractor-user-project-create')

    def get_success_url(self):
        contractor_id = self.request.user.id
        return reverse('contractor-user-profile-details', kwargs={'id': contractor_id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['image_formset'] = CreateImageFormSet(self.request.POST, self.request.FILES,
                                                       queryset=ImageModel.objects.none())
        else:
            data['image_formset'] = CreateImageFormSet(queryset=ImageModel.objects.none())
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        form.instance.contractor_user = self.request.user.contractor_user

        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()

            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.cleaned_data['image']
                    image_caption = image_form.cleaned_data.get('image_caption', '')
                    ImageModel.objects.create(contractor_project=self.object, image=image, image_caption=image_caption)

            return redirect(self.get_success_url())

        return self.form_invalid(form)


class ContractorProjectEditView(CustomLoginRequiredMixin, PrivateContractorProjectsViewsPermissionRequiredMixin, UpdateView):
    model = ContractorProjectModel
    form_class = ContractorProjectCreateForm
    template_name = 'accounts/contractors/project-edit.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        contractor_id = self.object.contractor_user.user.id
        return reverse_lazy('contractor-user-profile-details', kwargs={'id': contractor_id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        existing_images = ImageModel.objects.filter(contractor_project=self.object)
        extra_forms = max(0, 8 - existing_images.count())

        DynamicImageFormSet = modelformset_factory(
            ImageModel,
            form=ImageForm,
            extra=extra_forms,
            can_delete=True,
        )

        if self.request.POST:
            data['image_formset'] = DynamicImageFormSet(self.request.POST, self.request.FILES, queryset=existing_images)
        else:
            data['image_formset'] = DynamicImageFormSet(queryset=existing_images)

        # Modify the formset to remove delete checkbox if no image exists
        for form in data['image_formset']:
            # If the image instance doesn't exist, hide the delete checkbox

            form.fields['DELETE'].label = 'Изтрий'
            if not form.instance.pk:
                form.fields['DELETE'].widget = forms.HiddenInput()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()

            # Get all current images for the project
            existing_images = set(self.object.project_images.all())

            # Track images submitted via the formset
            submitted_images = set()

            for image_form in image_formset:
                if image_form.cleaned_data:
                    # Check if the form refers to an existing image
                    image_instance = image_form.instance
                    if image_instance and image_instance.pk:
                        # Existing image
                        if image_form.cleaned_data.get('DELETE'):  # If DELETE checkbox is checked
                            image_instance.delete()  # Delete the image if the checkbox is checked
                        else:
                            # Update the existing image
                            project_image = image_form.cleaned_data['image']
                            image_caption = image_form.cleaned_data.get('image_caption', '')

                            image_instance.image = project_image  # Update the image field
                            image_instance.image_caption = image_caption  # Update the caption field
                            image_instance.save()  # Save the updated image instance

                            submitted_images.add(image_instance)
                    else:
                        # New image (not existing in the database)
                        project_image = image_form.cleaned_data['image']
                        image_caption = image_form.cleaned_data.get('image_caption', '')

                        ImageModel.objects.create(
                            contractor_project=self.object,
                            image=project_image,
                            image_caption=image_caption
                        )

            # Remove images that were not re-submitted (images that are not in submitted_images)
            images_to_delete = existing_images - submitted_images
            for image in images_to_delete:
                image.delete()

            return redirect(self.get_success_url())

        return self.form_invalid(form)


class ContractorProjectDeleteView(CustomLoginRequiredMixin, PrivateContractorProjectsViewsPermissionRequiredMixin, DeleteView):
    model = ContractorProjectModel
    template_name = 'accounts/contractors/project-delete.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        contractor_id = self.object.contractor_user.user.id
        return reverse_lazy('contractor-user-profile-details', kwargs={'id': contractor_id})


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "accounts/common/login.html"


class CustomLogoutView(LogoutView):
    template_name = "accounts/common/logout.html"
    http_method_names = ['get', 'post', 'options']


class ContractorUserProfileDeleteView(PrivateProfilesViewsPermissionRequiredMixin, DeleteView):
    pass


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/common/password-change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password-change-done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/common/password-change-done.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/common/password-reset.html'
    email_template_name = 'emails/email-password-reset.html'
    success_url = reverse_lazy('password-reset-email-sent')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not BaseUserModel.objects.filter(email=email).exists():
            messages.error(self.request, 'Имейла не е валиден!')
            return redirect('password-reset')

        domain = get_current_site(self.request).domain
        protocol = 'http' if not self.request.is_secure() else 'https'
        user = BaseUserModel.objects.get(email=email)

        # Generate UID and Token
        uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        token = default_token_generator.make_token(user)


        email_subject = 'Създаване на нова парола'
        email_message = render_to_string(
            self.email_template_name,
            context={
                'uidb64': uid,
                'token': token,
                'protocol': protocol,
                'domain': domain,
        })


        send_mail(
            subject=email_subject,
            message=email_message,
            from_email='maistorbox@abv.com',
            recipient_list=['andon.go6ev@gmail.com', ],
            fail_silently=False,
        )

        return redirect('password-reset-email-sent')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/common/password-succesfully-sent-email.html'
    reverse_lazy = reverse_lazy('password-reset-email-sent')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/common/password-reset-confirm.html'
    form_class = CustomPasswordSetForm
    success_url = reverse_lazy('login')
