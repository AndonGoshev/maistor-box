# Generated by Django 5.1.2 on 2024-11-12 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_contractorusermodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractorusermodel',
            name='profile_image',
            field=models.ImageField(upload_to='contractor-users-profile-pictures'),
        ),
    ]