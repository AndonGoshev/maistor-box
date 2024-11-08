from django.contrib.auth.models import AbstractUser
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


class ContractorUserModel(models.Model):
    user = models.OneToOneField(
        BaseUserModel,
        on_delete=models.CASCADE,
    )

    phone_number = models.CharField()

    profile_image = models.ImageField(
        upload_to='media/users_profile_pictures',
    )

    regions = models.ManyToManyField(
        Regions,
        related_name='users',

    )

    specializations = models.ManyToManyField(
        Specializations,
        related_name='users',
    )