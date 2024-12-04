from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from urllib3 import request

from maistorbox.common.forms import ClientFeedbackForm
from maistorbox.common.models import ContractorPublicModel, ClientFeedbackModel
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

