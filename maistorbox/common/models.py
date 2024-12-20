from random import choices

from django.db import models

from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

from maistorbox.accounts.models import ContractorUserModel, BaseUserModel


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

    def average_rating(self):

        avg_rating = self.client_feedback.filter(approved=True).aggregate(Avg('rating'))['rating__avg']

        if avg_rating is None:
            return None

        return round(avg_rating)


class ClientFeedbackModel(models.Model):
    # This is the contractor who receives the feedback
    public_contractor = models.ForeignKey(
        to=ContractorPublicModel,
        on_delete=models.CASCADE,
        related_name='client_feedback',
    )

    # This is the user who gave the feedback
    client_user = models.ForeignKey(
        to=BaseUserModel,
        on_delete=models.CASCADE,
        # If t some point we need to retrieve the user's feedbacks we can do that by this related name
        related_name='feedbacks',
    )

    approved = models.BooleanField(
        default=False,
    )

    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
    )

    comment = models.TextField(
        blank=True,
        null=True,
        max_length=400,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
