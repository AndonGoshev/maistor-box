from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from maistorbox.common.models import ContractorPublicModel
from maistorbox.search_board.forms import ContractorSearchForm


class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contractor_search_form'] = ContractorSearchForm
        context['contractor'] = ContractorPublicModel.objects.all().order_by('-id')[:3]
        return context


class ContractorPublicProfileView(TemplateView):
    template_name = 'common/contractor-public-profile.html'

    def get_success_url(self):
        return reverse('contractor-public-profile', kwargs={'slug': self.kwargs['slug']})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        contractor = get_object_or_404(ContractorPublicModel, slug=slug)
        context['contractor'] = contractor

        return context

