from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from .models import ExpenseEntry
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    ExpenseEntrySerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API for user management.
    
    Endpoints:
    - POST /api/users/ — Create new user (signup)
    - GET /api/users/me/ — Get current user profile
    - PATCH /api/users/me/ — Update profile
    """
    
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """Use different serializer for different actions."""
        if self.action in ['create', 'update', 'partial_update']:
            return UserDetailSerializer #signup
        return UserSerializer #profile display
    
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Get or update current user profile."""
        user = request.user #Gets currently logged-in user.
        
        if request.method == 'PATCH': #partial update
            serializer = UserDetailSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ExpenseEntryViewSet(viewsets.ModelViewSet):
    """
    API for expense management.
    
    Endpoints:
    - GET /api/expenses/ — List all expenses (current user only)
    - POST /api/expenses/ — Create new expense
    - GET /api/expenses/{id}/ — Get expense details
    - PATCH /api/expenses/{id}/ — Update expense
    - DELETE /api/expenses/{id}/ — Delete expense
    - GET /api/expenses/summary/ — Get spending summary
    """
    
    serializer_class = ExpenseEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only return expenses for current user."""
        return ExpenseEntry.objects.filter(user=self.request.user)#users can ONLY see THEIR expenses.
    
    def perform_create(self, serializer):
        """Auto-assign current user when creating expense."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get spending summary.
        
        Returns: {
            "total_spent": 5000,
            "by_category": {"food": 2000, "transport": 1000},
            "count": 5
        }
        """
        expenses = self.get_queryset()
        
        total = sum(float(e.amount) for e in expenses)
        by_category = {}
        
        for expense in expenses:
            if expense.category not in by_category:
                by_category[expense.category] = 0
            by_category[expense.category] += float(expense.amount)
        
        return Response({
            'total_spent': total,
            'by_category': by_category,
            'count': expenses.count(),
            'monthly_income': float(request.user.monthly_income),
            'percentage_of_income': float((total / float(request.user.monthly_income) * 100) if request.user.monthly_income > 0 else 0)
        })