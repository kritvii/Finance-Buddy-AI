from django.contrib import admin
from .models import User, ExpenseEntry

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'monthly_income', 'savings_goal']
    list_filter = ['date_joined']
    search_fields = ['username', 'email']

@admin.register(ExpenseEntry)
class ExpenseEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'category', 'date']
    list_filter = ['category', 'date']
    search_fields = ['description', 'user__username']
