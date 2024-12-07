from django import forms

from maistorbox.common.models import ClientFeedbackModel, ContractorPublicModel
from maistorbox.mixins import FormsStylingMixin, ErrorMessagesTranslateMixin


class ClientFeedbackForm(forms.ModelForm):
    class Meta:
        model = ClientFeedbackModel
        exclude = ['public_contractor', 'client_user', 'approved', 'created_at']


class StyledClientFeedbackForm(ErrorMessagesTranslateMixin, FormsStylingMixin, ClientFeedbackForm):
    pass
