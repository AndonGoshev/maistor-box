from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class Company(models.Model):
    name = models.CharField(
        max_length=100,
    )

    phone_number = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
        max_length=100,
    )

    address = models.CharField(
        max_length=200,
    )

    instagram_page_url = models.URLField(
        max_length=200,
    )

    facebook_page_url = models.URLField(
        max_length=200,
    )

    linkedin_page_url = models.URLField(
        max_length=200,
    )

    def save(self, *args, **kwargs):
        if not self.pk and Company.objects.exists():
            raise ValidationError("The company is only one and you cannot add more!")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Message(models.Model):
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        related_name='messages',
    )

    sender = models.EmailField(
        max_length=200,
    )

    content = models.TextField(
        max_length=500,
        validators=[
            MinLengthValidator(20)
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

