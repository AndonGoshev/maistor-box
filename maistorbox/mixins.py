from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from maistorbox.accounts.models import BaseUserModel, ContractorUserModel, ContractorProjectModel


class FormsStylingMixin(forms.Form):
    PLACEHOLDER_TRANSLATION = {
        'username': 'Потребителско име...',
        'password': 'Парола...',
        'password1': 'Парола...',
        'password2': 'Потвърди парола...',
        'email': 'Имейл...',
        'first_name': 'Име...',
        'last_name': 'Фамилия...',
        'phone_number': 'Телефонен номер...',
        'profile_image': 'Качи профилна снимка...',
        'old_password': 'Стара парола...',
        'new_password1': 'Нова парола...',
        'new_password2': 'Потвърдете новата парола...',
        'project_name': 'Име на проекта',
        'project_description': 'Описание...',
        'image_caption': 'Описание за снимката...',
        'image': 'Снимка',
        'regions': 'Изберете в кои области или градове работите:',
        'specializations': 'Изберете специалисти:',
        'about_me': 'За мен...',
        'average_price_for_similar_project': 'Средна цена за подобен проект в лева:',
        'sender': 'Вашият имейл...',
        'content': 'Съобщение...',
        'rating': 'Изберete оценка...',
        'comment': '''Оставeтe коментар...(макс. 400 знака)''',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = self.PLACEHOLDER_TRANSLATION[field]
            self.fields[field].help_text = ''


# I'm using this approach for the translation because the other one requires installing things that are not really intuitive for Windows OS
class ErrorMessagesTranslateMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Field-specific custom error messages (applied first)
        field_messages = {
            'rating': {
                'required': 'Моля изберете нивото на майстора!',
            },
            'username': {
                'unique': "Потребител с това потребителско име вече съществува.",
                'invalid': "Невалидно потребителско име.",
            },
            'email': {
                'invalid': "Моля, въведете валиден имейл адрес.",
                'unique': "Този имейл вече е регистриран.",
            },
            'password1': {
                'required': "Паролата е задължителна.",
                'min_length': "Паролата трябва да бъде поне 8 символа.",
            },
            'password2': {
                'required': "Потвърдете паролата.",
                'password_mismatch': "Паролите не съвпадат.",
            },
            'first_name': {
                'required': "Това поле е задължително.",
                'max_length': "Името не може да бъде по-дълго от 30 символа.",
            },
            'last_name': {
                'required': "Това поле е задължително.",
                'max_length': "Фамилията не може да бъде по-дълга от 30 символа.",
            },
        }

        # Common error messages for all fields
        translated_messages = {
            'required': 'Това поле е задължително.',
            'invalid': 'Невалидна стойност.',
            'max_length': 'Тази стойност е твърде дълга.',
            'min_length': 'Тази стойност е твърде кратка.',
            'unique': 'Това поле трябва да бъде уникално.',
            'invalid_email': 'Моля, въведете валиден имейл адрес.',
            'password_mismatch': 'Паролите не съвпадат.',
            'max_value': 'Тази стойност е твърде голяма.',
            'min_value': 'Тази стойност е твърде малка.',
        }

        # Apply field-specific error messages first
        for field_name, messages in field_messages.items():
            if field_name in self.fields:
                self.fields[field_name].error_messages.update(messages)

        # Apply common messages last so that specific messages are not overwritten
        for field in self.fields.values():
            for error_code, message in translated_messages.items():
                field.error_messages.setdefault(error_code, message)

# This mixin is preventing not logged users to access contractors public profiles by entering their url
class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return redirect('login-required')


# TODO fix the comments because now we dont rely on the user authentication
# This mixin checks if a user is allowed to access a page.
# If the user isn’t logged in they can’t access the page.
# Even if they are logged in they won’t get access to someone else’s profile
# or pages related to it. It checks if the user from the request is the same
# as the one connected to the page.
class PrivateProfilesViewsPermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):

        def get_account():

            if request.user.user_type == 'contractor_user':
                account = get_object_or_404(ContractorUserModel, user__id=kwargs['id']).user

            else:
                account = get_object_or_404(BaseUserModel, pk=kwargs['id'])

            return account

        def get_page_url():
            return self.request.path

        # If the user is authenticated - get their account-object
        landed_account = get_account()

        # Check if the request user is the same as the one related to the pages
        # trying to be landed on.
        if request.user != landed_account:
            raise PermissionDenied(f'{request.user.username} tried to land on page '
                                   f'connected to account with id {landed_account.id} '
                                   f'by force browsing attack. The url of the page is - " {get_page_url()} " ')


        return super().dispatch(request, *args, **kwargs)

class PrivateContractorProjectsViewsPermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):

        if request.user.user_type != 'contractor_user':
            raise PermissionDenied(f'{request.user.username} user tried to land on private contractor project edit / delete page. The page is {self.request.path}.')

        project = get_object_or_404(ContractorProjectModel, pk=kwargs['id'])
        contractor_user = get_object_or_404(ContractorUserModel, user=request.user)

        if project.contractor_user != contractor_user:
            raise PermissionDenied(f'Contractor with id {contractor_user.id} and username {contractor_user.user.username} tried to land on another contractors project related view. The page is {self.request.path}.')

        return super().dispatch(request, *args, **kwargs)
