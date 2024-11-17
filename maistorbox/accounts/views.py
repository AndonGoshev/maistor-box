from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.base import kwarg_re
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.functional import keep_lazy
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView, DeleteView
from django.contrib import messages

from maistorbox.accounts.forms import BaseUserRegistrationForm, ContractorUserRegistrationForm, CustomLoginForm, \
    CustomPasswordChangeForm, CustomPasswordSetForm, CustomPasswordResetForm, ContractorProjectForm, ImageFormSet
from maistorbox.accounts.models import BaseUserModel, ContractorProject, ImageModel


class BaseUserRegistrationView(CreateView):
    form_class = BaseUserRegistrationForm
    template_name = 'accounts/regular-users/regular-user-registration.html'
    success_url = reverse_lazy('login')
    redirect_url = reverse_lazy('regular-user-registration')



class ContractorUserRegistrationView(CreateView):
    form_class = ContractorUserRegistrationForm
    template_name = 'accounts/contractors/contractor-registration.html'
    success_url = reverse_lazy('login')
    redirect_url = reverse_lazy('contractor-registration')


class ContractorProjectCreateView(CreateView):
    model = ContractorProject
    form_class = ContractorProjectForm
    template_name = 'accounts/contractors/contractor-user-upload-project.html'
    success_url = reverse_lazy('contractor-user-project-create')

    def get_success_url(self):
        contractor_id = self.request.user.contractor_user.id
        return reverse('contractor-user-profile-details', kwargs={'id': contractor_id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        #Initializing the image form_set
        if self.request.POST:
            data['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, queryset=ImageModel.objects.none())
        else:
            data['image_formset'] = ImageFormSet(queryset=ImageModel.objects.none())
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        #TODO check if it works with only .user or i should make it .contractor_user
        #Assigning project
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


class ContractorProjectDeleteView(DeleteView):
    model = ContractorProject
    template_name = 'accounts/contractors/project-delete.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        contractor_id = self.object.contractor_user.id
        return reverse_lazy('contractor-user-profile-details', kwargs={'id': contractor_id})









class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "accounts/common/login.html"

class CustomLogoutView(LogoutView):
    template_name = "accounts/common/logout.html"
    http_method_names = ['get', 'post', 'options']


class RegularUserProfileView(TemplateView):
    template_name = 'accounts/regular-users/regular-user-profile-details.html'

class UserProfileDeleteView(DeleteView):
    model = BaseUserModel
    success_url = reverse_lazy('home_page')
    template_name = 'accounts/common/profile-delete.html'
    pk_url_kwarg = 'id'


class ContractorUserProfileDetailsView(TemplateView):
    template_name = 'accounts/contractors/contractor-profile-details.html'


class ContractorUserProfileDeleteView(DeleteView):
    pass


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/common/password-change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password-change-done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/common/password-change-done.html'




class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/common/password-reset.html'
    email_template_name = 'accounts/common/email-password-reset.html'
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



        print(f"doamin - {domain}")
        print(f"protocol - {protocol}")
        print(f'user pk = {user.pk}')

        # Generate UID and Token
        uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        print(f"Generated UID: {uid}")  # Print UID to confirm it's correctly created
        token = default_token_generator.make_token(user)

        reset_link = f"{protocol}://{domain}{reverse_lazy('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})}"
        print(f"Generated reset link: {reset_link}")
        print(f"Token valid for user {user}: {default_token_generator.check_token(user, token)}")

        print(f"Email context: {{'uidb64': {uid}, 'token': {token}, 'protocol': {protocol}, 'domain': {domain}}}")

        email_subject = 'Създаване на нова парола'
        email_message = render_to_string(self.email_template_name, {
            'uidb64': uid,
            'token': token,
            'protocol': protocol,
            'domain': domain,
        })

        print(
            f"Context being passed to template: {{'uidb64': {uid}, 'token': {token}, 'protocol': {protocol}, 'domain': {domain}}}")
        send_mail(email_subject, email_message, 'from@example.com', [email])

        return redirect('password-reset-email-sent')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/common/password-succesfully-sent-email.html'
    reverse_lazy = reverse_lazy('password-reset-email-sent')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/common/password-reset-confirm.html'
    form_class = CustomPasswordSetForm
    success_url = reverse_lazy('login')


