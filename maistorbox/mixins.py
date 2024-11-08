from django import forms


class FormsStylingMixin(forms.Form):
    PLACEHOLDER_TRANSLATION = {
        'username': "Потребителско име...",
        'password': 'Парола...',
        'password1': 'Парола...',
        'password2': 'Потвърди парола...',
        'email': 'Имейл...',
        'first_name': 'Име...',
        'last_name': 'Фамилия...',
        'phone_number': 'Телефонен номер...',
        'profile_image': 'Качи профилна снимка...',
        'specializations': 'neshto si',
        'regions': 'neshto drugo si regioni'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:

            if field == 'regions':
                self.fields[field].label = 'Изберете в кои области или градове работите:'
                continue

            if field == 'specializations':
                self.fields[field].label = 'Изберете в кои специалности сте специалисти:'
                continue

            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = self.PLACEHOLDER_TRANSLATION[field]
            self.fields[field].help_text = ''

        if 'profile_image' in self.fields:
            self.fields['profile_image'].label = 'Качете профилна снимка:'


