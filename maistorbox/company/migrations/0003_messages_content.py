# Generated by Django 5.1.2 on 2024-12-05 15:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='content',
            field=models.TextField(default='MaistorBox', max_length=500, validators=[django.core.validators.MinLengthValidator(20)]),
            preserve_default=False,
        ),
    ]
