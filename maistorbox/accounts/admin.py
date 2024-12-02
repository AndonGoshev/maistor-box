from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from maistorbox.accounts.models import BaseUserModel, ContractorUserModel


class ContractorUserInLine(admin.StackedInline):
    model = ContractorUserModel
    extra = 1
    can_delete = False


class CustomUserAdmin(UserAdmin):
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
        ('User Type', {'fields': ('user_type',)}),
    )

    def get_inlines(self, request, obj=None):
        # If the user is a contractor, include the ContractorUserInLine
        if obj and obj.user_type == 'contractor_user':
            return [ContractorUserInLine]
        return []

    def save_model(self, request, obj, form, change):
        # Ensure the ContractorUserModel is created when saving the BaseUserModel if the user is a contractor
        if obj.user_type == 'contractor_user' and not hasattr(obj, 'contractor_user'):
            contractor_user = ContractorUserModel(user=obj)
            contractor_user.save()
        super().save_model(request, obj, form, change)


admin.site.register(BaseUserModel, CustomUserAdmin)


