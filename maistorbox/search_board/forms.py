from django import forms
from django.forms import ModelChoiceField

from maistorbox.accounts.models import Regions, Specializations


class ContractorSearchForm(forms.Form):
    regions = ModelChoiceField(
        queryset=Regions.objects.all(),
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'regions-search-field'}),
    )

    specializations = ModelChoiceField(
        queryset=Specializations.objects.all(),
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'specializations-search-field'}),
    )