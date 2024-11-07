from django import forms


class FormsStylingMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "username":
                self.fields[field].help_text = 'Полето може да съдържа само букви цифри и (@ . + - _)'
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = field