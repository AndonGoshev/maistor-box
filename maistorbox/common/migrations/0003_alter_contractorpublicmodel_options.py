# Generated by Django 5.1.2 on 2024-11-30 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_contractorpublicmodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contractorpublicmodel',
            options={'ordering': ('-contractor__created_at',)},
        ),
    ]