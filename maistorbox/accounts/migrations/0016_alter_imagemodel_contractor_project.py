# Generated by Django 5.1.2 on 2024-11-15 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_contractorproject_max_price_for_similar_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='contractor_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_images', to='accounts.contractorproject'),
        ),
    ]