from django.shortcuts import render
from django.views.generic import ListView

from maistorbox.common.models import ContractorPublicModel
from maistorbox.search_board.forms import ContractorSearchForm


class SearchBoardView(ListView):
    model = ContractorPublicModel
    template_name = 'search-board/search-board.html'
    context_object_name = 'contractors_list'
    form_class = ContractorSearchForm
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        search_form = self.get_form()

        if search_form.is_valid():
            selected_region = search_form.cleaned_data['regions']
            selected_specialization = search_form.cleaned_data['specializations']

        if selected_region:
            queryset = queryset.filter(contractor__regions=selected_region)
        if selected_specialization:
            queryset = queryset.filter(contractor__specializations=selected_specialization)

        queryset = queryset.distinct()

        return queryset

    def get_form(self):
        return self.form_class(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.get_form()
        return context
