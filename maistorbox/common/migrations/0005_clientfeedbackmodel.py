# Generated by Django 5.1.2 on 2024-12-01 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_contractorpublicmodel_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFeedbackModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('1', '2'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('comment', models.TextField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_feedback', to='common.contractorpublicmodel')),
            ],
        ),
    ]