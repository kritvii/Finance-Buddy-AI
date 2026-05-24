from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    monthly_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="User's monthly income in INR"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} (Rs.{self.monthly_income})'


class ExpenseEntry(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transport'),
        ('college', 'College Fees & Education'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities & Bills'),
        ('shopping', 'Shopping'),
        ('health', 'Health & Medical'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date'] # sort them by date, newest first.

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} on {self.category} ({self.date})"