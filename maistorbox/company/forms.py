from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm
from django.utils.timezone import now

from maistorbox import settings
from maistorbox.company.models import Message, CompanyModel
from maistorbox.mixins import FormsStylingMixin


class MessageForm(FormsStylingMixin ,ModelForm):
    class Meta:
        model = Message
        fields = ['sender_email', 'content', ]

    def save(self, commit=True, user=None):
        # Retrieve the single company instance
        company = CompanyModel.objects.first()
        if not company:
            raise forms.ValidationError('В момента не може да изпращате съобщения.')

        # Create a message instance
        message = super().save(commit=False)
        message.company = company
        message.created_at = now()

        sender_email = self.cleaned_data['sender_email']

        if commit:
            message.save()

        # Send an email
        send_mail(
            subject=f'Изпратено запитване от {sender_email}',
            message=message.content,
            from_email=sender_email,
            recipient_list=[settings.COMPANY_EMAIL ],
            fail_silently=False,
        )

        return message

