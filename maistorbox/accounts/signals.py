from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from maistorbox.accounts.models import ContractorUserModel
from maistorbox.common.models import ContractorPublicModel


@receiver(post_save, sender=ContractorUserModel)
def create_contractor_public_profile(sender, instance, created, **kwargs):
    if created:
        # Create the slug using first and last name (ensures uniqueness with a counter if necessary)
        first_name = instance.user.first_name.strip()
        last_name = instance.user.last_name.strip()
        slug = slugify(f"{first_name}-{last_name}")

        # Ensure slug uniqueness by appending a number if the slug already exists
        counter = 1
        original_slug = slug
        while ContractorPublicModel.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Create the public profile with just the slug
        ContractorPublicModel.objects.create(
            contractor=instance,
            slug=slug
        )