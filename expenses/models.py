from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, default=10000)

class ExpenseEntry(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('college', 'College'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
