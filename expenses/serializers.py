from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ExpenseEntry

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'monthly_income', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user info for signup and updates."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'monthly_income', 'password']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Create new user with hashed password."""
        user = User.objects.create_user(**validated_data)
        return user


class ExpenseEntrySerializer(serializers.ModelSerializer):
    """Serializer for ExpenseEntry model."""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = ExpenseEntry
        fields = ['id', 'user', 'user_id', 'amount', 'category', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        """Create expense entry."""
        return ExpenseEntry.objects.create(**validated_data)