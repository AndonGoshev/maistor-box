from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageSizeValidator:
    def __init__(self, max_size_mb):
        self.max_size_mb = max_size_mb

    @property
    def max_size_mb(self):
        return self._max_size_mb

    @max_size_mb.setter
    def max_size_mb(self, value):
        if not value:
            self.max_size_mb = 5
        self._max_size_mb = value

    def __call__(self, image, *args, **kwargs):
        file_size = image.size

        if file_size > self.max_size_mb * 1024 * 1024:
            raise ValidationError('Изображението не може да бъде по-голямо от 5MB.')



@deconstructible()
class PhoneNumberValidator:
    def __init__(self, min_length):
        self._min_length = min_length

    @property
    def min_length(self):
        return self._min_length

    @min_length.setter
    def min_length(self, value):
        self._min_length = value


    def __call__(self, phone_number):

        if len(phone_number) < self.min_length:
            raise ValidationError(f'Телефонния номер трябва да садържа минимум {self._min_length} цифри!')

        if not phone_number.isdigit():
            raise ValidationError('Телефонния номер може да садържа само цифри!')