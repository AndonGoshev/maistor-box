from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from maistorbox.accounts.choices import UserTypeChoice


class Regions(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Specializations(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseUserModel(AbstractUser):
    user_type = models.CharField(
        choices=UserTypeChoice,
        default=UserTypeChoice.REGULAR_USER,
        max_length=50,
    )

    email = models.EmailField(unique=True)


class ContractorUserModel(models.Model):
    user = models.OneToOneField(
        BaseUserModel,
        on_delete=models.CASCADE,
        related_name='contractor_user',
    )

    about_me = models.TextField(
        blank=True,
        null=True,
    )

    phone_number = models.CharField()

    profile_image = models.ImageField(
        upload_to='contractor-users-profile-pictures',
    )

    regions = models.ManyToManyField(
        Regions,
        related_name='regions',
    )

    specializations = models.ManyToManyField(
        Specializations,
        related_name='specializations',
    )


class ContractorProject(models.Model):
    project_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    project_description = models.TextField(
        max_length=1000,
    )

    min_price_for_similar_project = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    max_price_for_similar_project = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    contractor_user = models.ForeignKey(
        to=ContractorUserModel,
        on_delete=models.CASCADE,
        related_name='projects',
    )

    def clean(self):
        if self.min_price_for_similar_project and self.max_price_for_similar_project:
            if self.min_price_for_similar_project > self.max_price_for_similar_project:
                raise ValidationError({
                    'min_price_for_similar_project': 'Минималната цена не може да бъде по-висока от максималната.',
                    'max_price_for_similar_project': 'Максималната цена не може да бъде по-ниска от минималната.'
                })


class ImageModel(models.Model):
    image = models.ImageField()

    image_caption = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    contractor_project = models.ForeignKey(
        to=ContractorProject,
        on_delete=models.CASCADE,
        related_name='project_images',
    )
