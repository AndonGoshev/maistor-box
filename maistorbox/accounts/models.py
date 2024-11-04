from django.contrib.auth.models import AbstractUser
from django.db import models

from maistorbox.accounts.choices import UserTypeChoice


class Specializations(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True,
    )

    def __str__(self):
        return self.name


class Regions(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True,
    )

    def __str__(self):
        return self.name


class BaseUserModel(AbstractUser):
    user_type = models.CharField(
        max_length=20,
        choices=UserTypeChoice,
        default=UserTypeChoice.REGULAR_USER
    )


class RegularUserModel(BaseUserModel):
    pass


class ContractorUser(BaseUserModel):
    regions = models.ManyToManyField(
        Regions,
        blank=True,
    )
    specializations = models.ManyToManyField(
        Specializations,
        blank=True,
    )
    profile_picture = models.ImageField(
        upload_to='media/media'
    )

    def __str__(self):
        return f'{self.username} (Майстор)'


class ProjectImage(models.Model):
    contractor = models.ForeignKey(
        to=ContractorUser,
        on_delete=models.CASCADE,
        related_name='contractor_projects'
    )
    image = models.ImageField(
        upload_to='media/user_images',
        blank=True,
        null=True,
    )

