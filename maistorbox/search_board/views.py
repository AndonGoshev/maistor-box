from django.db.models.functions import Random
from django.views.generic import ListView

from maistorbox.accounts.models import Region, Specialization
from maistorbox.helpers import select_all_option_instance_id
from maistorbox.common.models import ContractorPublicModel
from maistorbox.mixins import CustomLoginRequiredMixin
from maistorbox.search_board.forms import ContractorSearchForm


class SearchBoardView(CustomLoginRequiredMixin, ListView):
    model = ContractorPublicModel
    template_name = 'search-board/search-board.html'
    context_object_name = 'contractors_list'
    form_class = ContractorSearchForm
    paginate_by = 12

    def get_queryset(self):
        contractors_for_displaying = super().get_queryset()


        search_form = self.get_form()

        if search_form.is_valid():
            selected_region = search_form.cleaned_data['regions']
            selected_specialization = search_form.cleaned_data['specializations']

        if selected_region and selected_region != select_all_option_instance_id(Region):
            contractors_for_displaying = contractors_for_displaying.filter(contractor__regions=selected_region)

        if selected_specialization and selected_specialization != select_all_option_instance_id(Specialization) :
            contractors_for_displaying = contractors_for_displaying.filter(contractor__specializations=selected_specialization)

        contractors_for_displaying = contractors_for_displaying.order_by(Random())

        return contractors_for_displaying

    def get_form(self):
        return self.form_class(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.get_form()
        return context
