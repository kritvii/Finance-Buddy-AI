import pandas as pd
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from expenses.models import ExpenseEntry

class SpendingAnalytics:
    """
    Analytics engine using Pandas.
    Analyzes user spending patterns.
    """
    
    def __init__(self, user, days=30): #This is the constructor __init__
        """
    Initialize analytics for a user's expenses.

    Args:
        user: The user whose expenses will be analyzed.
        days (int): Number of past days to include. Default is 30.
    """
        self.user = user
        self.days = days
        self.expenses = self._get_expenses_dataframe()
    
    def _get_expenses_dataframe(self): #Get Expenses as DataFrame
        """Convert database expenses to Pandas DataFrame."""
        cutoff_date = timezone.now().date() - timedelta(days=self.days)
        
        expenses = ExpenseEntry.objects.filter(
            user=self.user,
            date__gte=cutoff_date
        ).values('date', 'amount', 'category', 'description')
        
        if expenses.exists():
            df = pd.DataFrame.from_records(expenses)
            df['amount'] = pd.to_numeric(df['amount'])
            return df
        else:
            return pd.DataFrame(columns=['date', 'amount', 'category', 'description'])
        
    #Method 1: Total Spending
    def get_total_spending(self):
        """Total spending in period."""
        if self.expenses.empty:
            return Decimal('0')
        return Decimal(str(self.expenses['amount'].sum()))
    
    #Method 2: By Category
    def get_by_category(self):
        """Breakdown by category."""
        if self.expenses.empty:
            return {}
        
        grouped = self.expenses.groupby('category')['amount'].sum()
        return {
            category: float(amount) 
            for category, amount in grouped.items()
        }
    
    #Method 3: Daily Average

    def get_daily_average(self):
        """Average spending per day."""
        if self.expenses.empty:
            return Decimal('0')
        
        total_days = len(self.expenses['date'].unique())
        if total_days == 0:
            return Decimal('0')
        
        return Decimal(str(self.expenses['amount'].sum() / total_days))
    
    #Method 4: Category Percentage
    def get_category_percentage(self):
        """Percentage of total by category."""
        if self.expenses.empty:
            return {}
        
        by_category = self.get_by_category()
        total = self.get_total_spending()
        
        if total == 0:
            return {}
        
        return {
            cat: float((amount / float(total)) * 100)
            for cat, amount in by_category.items()
        }
    
    #Method 5: Full Report
    def get_full_report(self):
        """Get complete analytics summary."""
        return {
            'total_spent': float(self.get_total_spending()),
            'daily_average': float(self.get_daily_average()),
            'by_category': self.get_by_category(),
            'category_percentage': self.get_category_percentage(),
            'expense_count': len(self.expenses),
            'monthly_income': float(self.user.monthly_income),
            'percentage_of_income': float((float(self.get_total_spending()) / float(self.user.monthly_income) * 100) if self.user.monthly_income > 0 else 0)
        }