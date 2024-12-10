from django.db import models


class UserTypeChoice(models.TextChoices):
    REGULAR_USER = 'regular_user', 'Regular User'
    CONTRACTOR_USER = 'contractor_user', 'Contractor User'
