# Generated by Django 5.1.2 on 2024-12-06 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_remove_clientfeedbackmodel_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientfeedbackmodel',
            old_name='contractor',
            new_name='public_contractor',
        ),
    ]
