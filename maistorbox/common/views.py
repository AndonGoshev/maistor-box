from lib2to3.fixes.fix_input import context

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from urllib3 import request

from maistorbox.common.forms import ClientFeedbackForm
from maistorbox.common.models import ContractorPublicModel, ClientFeedbackModel
from maistorbox.company.forms import MessageForm
from maistorbox.company.models import Company
from maistorbox.company.views import MessageFormView
from maistorbox.mixins import CustomLoginRequiredMixin
from maistorbox.search_board.forms import ContractorSearchForm


class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contractor_search_form'] = ContractorSearchForm
        context['contractor'] = ContractorPublicModel.objects.all().order_by('-id')[:3]

        return context


class AboutUsView(TemplateView):
    template_name = 'common/about-us.html'


class ContactsView(View):
    template_name = 'common/contacts.html'

    def get_context(self, form=None):
        """
        Prepares the context for the page, including:
        - Company details for a specific section.
        - Message form for another section.
        """
        company = Company.objects.first()  # Fetch the single company instance
        context = {
            'company': company,  # Pass company info for the relevant section
            'form': form or MessageForm(),  # Use the given form or create a new one
        }
        return context

    def get(self, request):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                form.save(user=request.user)  # Save the form and send the email
                return redirect('sent_successfully')  # Redirect to success page

            except forms.ValidationError as e:
                form.add_error(None, e.message)  # Add an error to the form

        # If the form is invalid, re-render the page with the form and errors
        context = self.get_context(form)
        return render(request, self.template_name, context)


class SentSuccessfullyView(TemplateView):
    template_name = 'common/sent-successfully.html'

class ContractorPublicProfileView(CustomLoginRequiredMixin, TemplateView):
    template_name = 'common/contractor-public-profile.html'

    def get_success_url(self):
        return reverse('contractor-public-profile', kwargs={'slug': self.kwargs['slug']})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']
        contractor = get_object_or_404(ContractorPublicModel, slug=slug)
        context['contractor'] = contractor

        # client_user = request.user
        context['feedback_form'] = ClientFeedbackForm
        context['feedback'] = ClientFeedbackModel.objects.filter(contractor=contractor)

        return context

class LoginRequiredView(TemplateView):
    template_name = 'common/login-required.html'

