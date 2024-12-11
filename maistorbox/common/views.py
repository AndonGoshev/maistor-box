from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, FormView

from maistorbox.common.forms import ClientFeedbackForm, StyledClientFeedbackForm
from maistorbox.common.models import ContractorPublicModel, ClientFeedbackModel
from maistorbox.company.forms import MessageForm
from maistorbox.company.models import CompanyModel
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
    template_name = 'common/static_pages/about-us.html'


class ContactsView(View):
    template_name = 'common/static_pages/contacts.html'

    def get_context(self, form=None):

        company = CompanyModel.objects.first()
        context = {
            'company': company,
            'form': form or MessageForm(),
        }
        return context

    def get(self, request):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                form.save(user=request.user)
                return redirect('sent_successfully')

            except forms.ValidationError as e:
                form.add_error(None, e.message)

        context = self.get_context(form)
        return render(request, self.template_name, context)


class SentSuccessfullyView(TemplateView):
    template_name = 'common/sent-successfully.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contractor_slug = self.request.GET.get('contractor_slug')
        if contractor_slug:
            contractor_profile_url = reverse('contractor-public-profile', kwargs={'slug': contractor_slug})
            context['contractor_profile_url'] = contractor_profile_url
        return context

class ContractorPublicProfileView(FormsStylingMixin, CustomLoginRequiredMixin, FormView):
    template_name = 'common/contractor_related_and_feedbacks/contractor-public-profile.html'
    form_class = StyledClientFeedbackForm

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

        success_url = reverse('sent_successfully') + f'?contractor_slug={self.public_contractor.slug}'
        return redirect(success_url)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['public_contractor'] = self.public_contractor
        context['feedbacks'] = self.public_contractor.client_feedback.filter(approved=True)

        return context


class LoginRequiredView(TemplateView):
    template_name = 'common/login-required.html'

