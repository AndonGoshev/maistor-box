from django.db.models import TextChoices


class RatingNumberChoices(TextChoices):
    ONE = '1', '2'
    TWO = '2', '2'
    THREE = '3', '3'
    FOUR = '4', '4'
    FIVE = '5', '5'