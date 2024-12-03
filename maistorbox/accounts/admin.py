from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ValidationError

from maistorbox.accounts.forms import ContractorUserRegistrationForm
from maistorbox.accounts.models import BaseUserModel, ContractorUserModel


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
        'username',
        'last_name',
        'email',
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

    def save_model(self, request, obj, form, change):

        if obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(ContractorUserModel)
class ContractorUserModelAdmin(ModelAdmin):
    model = ContractorUserModel
    list_display = ('user', 'phone_number', 'profile_image', 'created_at')

