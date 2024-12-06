from django.contrib import admin

from maistorbox.company.models import Company, Message


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company

    list_display = ('name', 'phone_number', 'email', 'address', 'instagram_page_url', 'facebook_page_url', 'linkedin_page_url')


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    model = Message

    list_display = ('sender', )
    list_filter = ('sender', 'created_at', )
    search_fields = ('sender', 'created_at')

    ordering = ('-created_at', )