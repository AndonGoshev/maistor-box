from django.contrib import admin

from maistorbox.common.models import ContractorPublicModel


@admin.register(ContractorPublicModel)
class ContractorPublicModelAdmin(admin.ModelAdmin):
    model = ContractorPublicModel
    fields = ('contractor', 'slug')

    search_fields = ('contractor__id', 'slug')