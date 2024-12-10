from django.contrib import admin

from maistorbox.company.models import CompanyModel, Message


@admin.register(CompanyModel)
class CompanyAdmin(admin.ModelAdmin):
    model = CompanyModel

    list_display = ('name', 'phone_number', 'email', 'address', 'instagram_page_url', 'facebook_page_url', 'linkedin_page_url')


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    model = Message

    list_display = ('content' , 'sender_email', 'created_at')
    list_filter = ('created_at', )
    search_fields = ('sender_email', 'created_at')

    ordering = ('-created_at', )