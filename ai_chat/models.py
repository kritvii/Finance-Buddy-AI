from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatMessage(models.Model):
    """
    Store chat history between user and AI.
    """
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )
    
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} ({self.role}): {self.message[:50]}"