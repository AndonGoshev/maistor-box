import logging

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from unidecode import unidecode

from maistorbox.accounts.models import ContractorUserModel, BaseUserModel
from maistorbox.common.models import ContractorPublicModel
from maistorbox.settings import COMPANY_EMAIL


@receiver(post_save, sender=BaseUserModel)
def send_welcoming_email(sender, instance, created, **kwargs):
    if created:
        print(f'message send from {COMPANY_EMAIL}')
        print(f"Sending welcome email to: {instance.email}")
        send_mail(
            subject=f'Успешна регистрация!',
            message='Поздравления! Вие успешно се регистрирахте в най-разпознаваемия сайт за майстори!',
            from_email=COMPANY_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )


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
