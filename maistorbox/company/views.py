from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.generic import FormView

from maistorbox.company.forms import MessageForm
from maistorbox.company.models import Company


class MessageFormView(FormView):
    form_class = MessageForm
    template_name = 'company/message-form.html'

    def form_valid(self, form):
        company = Company.objects.first()
        if not company:
            form.add_error(None, 'В момента не може да изпращате съобщения.')
            return self.form_invalid(form)

        message = form.save(commit=False)
        message.company = company
        message.created_at = now()

        message.save()

        if self.request.user.is_authenticated and self.request.user.user_type == 'contractor_user':
            sender_username = self.request.user.contractor_user.email
        else:
            sender_username = None

        send_mail(
            subject=f'Нова съобщение от {message.sender}',
            message=message.content,
            from_email=sender_username,
            recipient_list=(company.email)
        )

        return super().form_valid(form)

    def get_success_url(self):
        return redirect('home_page')

