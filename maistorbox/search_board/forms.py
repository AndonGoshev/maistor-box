from django import forms
from django.forms import ModelChoiceField

from maistorbox.accounts.models import Region, Specialization


class ContractorSearchForm(forms.Form):
    regions = ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'regions-search-field'}),
    )

    specializations = ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'specializations-search-field'}),
    )