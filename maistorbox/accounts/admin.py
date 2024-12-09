from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ValidationError

from maistorbox.accounts.forms import ContractorUserRegistrationForm
from maistorbox.accounts.models import BaseUserModel, ContractorUserModel, ContractorProjectModel, ImageModel, \
    Specialization, Region


@admin.register(BaseUserModel)
class BaseUserModelAdmin(ModelAdmin):
    model = BaseUserModel

    list_display = (
        'username',
        'date_joined',
        'user_type',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'date_joined',
        'user_type',
        'is_active',
        'is_staff',
    )

    search_fields = (
        'username',
        'email',
    )

    ordering = ('-date_joined', )

    fieldsets = (
        ('User credentials', {'fields': ('username', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )}),
        ('user types', {'fields': ('user_type',)}),
    )


    # We are overriding this method to ensure that if a superuser
    # tries to change_user will not see the password at all
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'password' in form.base_fields:
            form.base_fields['password'].widget = forms.HiddenInput()

        return form


@admin.register(ContractorUserModel)
class ContractorUserModelAdmin(ModelAdmin):
    model = ContractorUserModel
    list_display = ('user', 'phone_number', 'profile_image', 'created_at')

@admin.register(ContractorProjectModel)
class ContractorProjectModelAdmin(admin.ModelAdmin):
    model = ContractorProjectModel
    list_display = ('project_name', 'average_price_for_similar_project', 'contractor_user')
    list_filter = ('project_name', 'contractor_user')
    search_fields = ('project_name', 'contractor_user')

    fieldsets = (
        ('Project data', {'fields': ('project_name', 'project_description', 'average_price_for_similar_project')}),
        ('Contractor Relationship', {'fields': ('contractor_user',)}),
    )


@admin.register(ImageModel)
class ImageModelAdmin(ModelAdmin):
    model = ImageModel
    list_display = ('image', 'image_caption', 'contractor_project_id')
    list_filter = ('image', 'contractor_project', 'contractor_project_id')
    search_fields = ('image', 'contractor_project__contractor_user')

    fieldsets = (
        ('Image data', {'fields': ('image', 'image_caption', )}),
        ('Project Relationship', {'fields': ('contractor_project',)}),
    )


@admin.register(Specialization)
class SpecializationsAdmin(ModelAdmin):
    model = Specialization
    fields = ('name', )

@admin.register(Region)
class RegionsAdmin(ModelAdmin):
    model = Specialization
    fields = ('name', )