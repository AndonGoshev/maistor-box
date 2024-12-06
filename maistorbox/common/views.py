from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView

from maistorbox.common.forms import ClientFeedbackForm
from maistorbox.common.models import ContractorPublicModel, ClientFeedbackModel
from maistorbox.company.forms import MessageForm
from maistorbox.company.models import Company
from maistorbox.mixins import CustomLoginRequiredMixin, FormsStylingMixin
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

class ContractorPublicProfileView(CustomLoginRequiredMixin, FormsStylingMixin, FormView):
    template_name = 'common/contractor-public-profile.html'
    form_class = ClientFeedbackForm

    def dispatch(self, request, *args, **kwargs):
        self.client_user = request.user
        self.public_contractor = get_object_or_404(ContractorPublicModel, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('sent_successfully')

    def form_valid(self, form):
        feedback_form = form.save(commit=False)
        feedback_form.public_contractor = self.public_contractor
        feedback_form.client_user = self.client_user
        feedback_form.created_at = now()

        feedback_form.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['public_contractor'] = self.public_contractor
        context['feedbacks'] = self.public_contractor.client_feedback.filter(approved=True)

        return context



















    # def get_object(self):
    #     slug = self.kwargs['slug']
    #     return get_object_or_404(ContractorPublicModel, slug=slug)
    #
    # def get_success_url(self):
    #     return reverse('contractor-public-profile', kwargs={'slug': self.kwargs['slug']})
    #
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     slug = self.kwargs['slug']
    #     contractor = get_object_or_404(ContractorPublicModel, slug=slug)
    #     context['contractor'] = contractor
    #
    #     # client_user = request.user
    #     context['feedback_form'] = ClientFeedbackForm
    #     context['feedback'] = ClientFeedbackModel.objects.filter(contractor=contractor)
    #
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()  # Fetch contractor instance
    #     form = ClientFeedbackForm(request.POST)
    #     if form.is_valid():
    #         feedback = form.save(commit=False)
    #         feedback.contractor = self.object
    #         feedback.client_user = request.user
    #         feedback.save()
    #         return redirect(self.get_success_url())
    #     # Re-render page with form errors
    #     context = self.get_context_data()
    #     context['feedback_form'] = form
    #     return self.render_to_response(context)

class LoginRequiredView(TemplateView):
    template_name = 'common/login-required.html'

