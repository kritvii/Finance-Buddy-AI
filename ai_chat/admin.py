from django.contrib import admin

# Register your models here.
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'message', 'created_at')
    list_filter = ('role', 'user')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)