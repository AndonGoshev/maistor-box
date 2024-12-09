from django.contrib import admin

from maistorbox.common.models import ContractorPublicModel, ClientFeedbackModel


@admin.register(ContractorPublicModel)
class ContractorPublicModelAdmin(admin.ModelAdmin):
    model = ContractorPublicModel
    fields = ('contractor', 'slug')
    list_display = ('contractor', 'slug')

    search_fields = ('contractor__id', 'slug')


@admin.register(ClientFeedbackModel)
class ClientFeedbackModelAdmin(admin.ModelAdmin):
    model = ClientFeedbackModel
    fields = ('rating', 'comment', 'approved', 'public_contractor', 'client_user')
    list_display = ('comment', 'rating','public_contractor', 'approved')

    search_fields = ('public_contractor__slug', 'rating', )

    readonly_fields = ('public_contractor', 'client_user')
