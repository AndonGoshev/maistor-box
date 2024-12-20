from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from maistorbox.accounts.choices import UserTypeChoice
from maistorbox.accounts.validators import ImageSizeValidator, PhoneNumberValidator


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Specialization(models.Model):
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

    phone_number = models.CharField(
        max_length=20,
        validators=[
            PhoneNumberValidator(5),
        ]
    )

    profile_image = models.ImageField(
        upload_to='contractor-users-profile-pictures',
        validators=[
            ImageSizeValidator(5),
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    regions = models.ManyToManyField(
        Region,
        related_name='regions',
    )

    specializations = models.ManyToManyField(
        Specialization,
        related_name='specializations',
    )

    available_for_new_projects = models.BooleanField(
        default=True,
    )

    weekday_start_time = models.TimeField(null=True, blank=True)
    weekday_end_time = models.TimeField(null=True, blank=True)

    weekend_start_time = models.TimeField(null=True, blank=True)
    weekend_end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'Contractor with id: {self.id} '



class ContractorProjectModel(models.Model):
    project_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    project_description = models.TextField(
        max_length=1000,
    )

    average_price_for_similar_project = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
        ]
    )

    contractor_user = models.ForeignKey(
        to=ContractorUserModel,
        on_delete=models.CASCADE,
        related_name='projects',
    )


class ImageModel(models.Model):
    image = models.ImageField(
        upload_to='contractor-project-images',
    )

    image_caption = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    contractor_project = models.ForeignKey(
        to=ContractorProjectModel,
        on_delete=models.CASCADE,
        related_name='project_images',
    )
