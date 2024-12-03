from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from unidecode import unidecode

from maistorbox.accounts.models import ContractorUserModel
from maistorbox.common.models import ContractorPublicModel


@receiver(post_save, sender=ContractorUserModel)
def create_contractor_public_profile(sender, instance, created, **kwargs):
    if created:
        # Create the slug using first and last name (ensures uniqueness with a counter if necessary)
        first_name = instance.user.first_name.strip()
        last_name = instance.user.last_name.strip()

        if first_name and last_name:
            slug = f"{first_name}-{last_name}".strip()
        else:
            slug = instance.user.username.strip()
        transliterated_name = unidecode(slug)

        final_slug = slugify(transliterated_name)

        # Ensure slug uniqueness by appending a number if the slug already exists
        counter = 1
        original_slug = final_slug
        while ContractorPublicModel.objects.filter(slug=final_slug).exists():
            final_slug = f"{original_slug}-{counter}"
            counter += 1

        # Create the public profile with just the slug
        ContractorPublicModel.objects.create(
            contractor=instance,
            slug=final_slug
        )