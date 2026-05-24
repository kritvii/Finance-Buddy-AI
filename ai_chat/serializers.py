from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatMessage model.
    
    Converts ChatMessage database objects to JSON.
    
    What it does:
    - Takes a ChatMessage from database
    - Converts it to JSON that frontend can understand
    
    Example:
    Database: ChatMessage(role='user', message='Am I overspending?', created_at=...)
    JSON: {
        "id": 1,
        "role": "user",
        "message": "Am I overspending?",
        "created_at": "2026-05-22T00:00:00Z"
    }
    """
    
    class Meta:   #Used to configure serializer.
        model = ChatMessage
        # These are the fields to include in JSON
        fields = ['id', 'role', 'message', 'created_at']
        # These fields can't be edited (read-only)
        read_only_fields = ['id', 'role', 'created_at']