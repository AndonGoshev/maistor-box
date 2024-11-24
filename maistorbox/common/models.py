from django.db import models

from django.db import models
from django.utils.text import slugify

from maistorbox.accounts.models import ContractorUserModel


class ContractorPublicModel(models.Model):
    contractor = models.OneToOneField(
        ContractorUserModel,
        on_delete=models.CASCADE,
        related_name='public_profile',
    )

    slug = models.SlugField(
        unique=True,
        max_length=100,
    )

    def __str__(self):
        return f"Public Profile for {self.contractor.user.first_name} {self.contractor.user.last_name}"
