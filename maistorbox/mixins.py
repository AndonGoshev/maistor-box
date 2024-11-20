from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from maistorbox.accounts.models import BaseUserModel


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
        'min_price_for_similar_project': 'Минимална цена за подобен проект в лева...',
        'max_price_for_similar_project': 'Максимална цена за подобен проект в лева...',
        'image': 'Снимка',
        'regions': 'Изберете в кои области или градове работите:',
        'specializations': 'Изберете специалисти:',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == "max_price_for_similar_project" or field == "min_price_for_similar_project":
                self.fields[field].help_text = self.PLACEHOLDER_TRANSLATION[field]
                self.fields[field].label = ''
                continue

            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = self.PLACEHOLDER_TRANSLATION[field]
            self.fields[field].help_text = ''

        if 'profile_image' in self.fields:
            self.fields['profile_image'].label = 'Моля качете профилна снимка:'


# I'm using this approach for the translation because the other one requires installing things that are not really intuitive for Windows OS
class ErrorMessagesTranslateMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Field-specific custom error messages (applied first)
        field_messages = {
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


class MinPriceMaxPriceValidationMixin:
    def clean(self):
        cleaned_data = super().clean()

        min_price = cleaned_data.get('min_price_for_similar_project')
        max_price = cleaned_data.get('max_price_for_similar_project')

        if min_price and max_price:
            if min_price > max_price:

                raise ValidationError({
                    'min_price_for_similar_project': 'Минималната цена не може да бъде по-висока от максималната.',
                    'max_price_for_similar_project': 'Максималната цена не може да бъде по-ниска от минималната.'
                })

        return cleaned_data