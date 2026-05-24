from django.contrib import admin

# Register your models here.
from .models import User, ExpenseEntry

@admin.register(User)  #Show this model inside Django admin panel
class UserAdmin(admin.ModelAdmin):
    """Admin interface for Users."""
    list_display = ('username', 'email', 'monthly_income', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('username', 'email') #searchbar functionality 
    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Financial Info', {
            'fields': ('monthly_income',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )


@admin.register(ExpenseEntry)
class ExpenseEntryAdmin(admin.ModelAdmin):
    """Admin interface for Expenses."""
    list_display = ('user', 'amount', 'category', 'date', 'description')
    list_filter = ('category', 'date', 'user')
    search_fields = ('user__username', 'description') #user__username-->Go through ForeignKey relationship and search username field
    date_hierarchy = 'date'
    fieldsets = (
        ('Expense Info', {
            'fields': ('user', 'amount', 'category', 'description')
        }),
        ('Date Info', {
            'fields': ('date',),
        }),
    )

    