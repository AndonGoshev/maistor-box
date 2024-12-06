from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm
from django.utils.timezone import now

from maistorbox.company.models import Message, Company
from maistorbox.mixins import FormsStylingMixin


class MessageForm(FormsStylingMixin ,ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'content', ]

    def save(self, commit=True, user=None):
        # Retrieve the single company instance
        company = Company.objects.first()
        if not company:
            raise forms.ValidationError('В момента не може да изпращате съобщения.')

        # Create a message instance
        message = super().save(commit=False)
        message.company = company
        message.created_at = now()

        if commit:
            message.save()

        # Determine sender username
        sender_username = None
        if user and user.is_authenticated and getattr(user, 'user_type', None) == 'contractor_user':
            sender_username = getattr(user.contractor_user, 'email', None)

        # Send an email
        send_mail(
            subject=f'Ново съобщение от {message.sender}',
            message=message.content,
            from_email=sender_username,
            recipient_list=[company.email],
        )

        return message

