from django import forms

from maistorbox.common.models import ClientFeedbackModel, ContractorPublicModel


class ClientFeedbackForm(forms.ModelForm):
    class Meta:
        model = ClientFeedbackModel
        exclude = ['contractor', 'client_user', 'approved']

    def save(self, commit=True):
        contractor = ContractorPublicModel.objects.filter()