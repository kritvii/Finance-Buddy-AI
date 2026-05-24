from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ChatMessage
from .serializers import ChatMessageSerializer
from .services import FinancialAdvisor


class ChatViewSet(viewsets.ViewSet):
    """
    API endpoints for AI chat.
    
    What this does:
    - Handles chat messages from frontend
    - Sends to Gemini AI
    - Saves conversation history
    - Returns AI response
    
    Endpoints:
    - GET /api/chat/ — Get chat history
    - POST /api/chat/chat/ — Send message, get response
    - POST /api/chat/roast/ — Get spending roast
    """
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        GET /api/chat/
        
        Get all past chat messages for current user.
        
        Why store chat history?
        - Users can scroll back
        - Gemini can use context from previous messages
        - We can learn what users ask
        
        Returns:
            List of all chat messages for this user
        """
        # Get all messages for current user, ordered by date
        messages = ChatMessage.objects.filter(user=request.user)
        # Convert to JSON using serializer
        serializer = ChatMessageSerializer(messages, many=True)
        # Return JSON
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """
        POST /api/chat/chat/
        
        Main chat endpoint. User sends message, gets AI response.
        
        Request body:
        {
            "message": "Am I overspending?"
        }
        
        Response:
        {
            "user_message": "Am I overspending?",
            "ai_response": "Based on your data, you spent ₹2000...",
            "saved": true
        }
        
        What happens:
        1. User sends message
        2. Save message to database (role='user')
        3. Create FinancialAdvisor with user's data
        4. Get AI response from Gemini
        5. Save AI response to database (role='assistant')
        6. Return both messages to frontend
        """
        
        # Get the message from request
        message_text = request.data.get('message')
        
        # Check if message is provided
        if not message_text:
            return Response(
                {'error': 'Message field required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Step 1: Save user's message to database
        ChatMessage.objects.create(
            user=request.user,
            role='user',
            message=message_text
        )
        
        # Step 2: Get AI response from Gemini
        try:
            # Create advisor with current user
            advisor = FinancialAdvisor(request.user)
            # Get response based on user's actual spending data
            ai_response = advisor.get_advice(message_text)
        except Exception as e:
            # If Gemini API fails, return error
            return Response(
                {'error': f'AI service error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Step 3: Save AI response to database
        ChatMessage.objects.create(
            user=request.user,
            role='assistant',
            message=ai_response
        )
        
        # Step 4: Return both messages to frontend
        return Response({
            'user_message': message_text,
            'ai_response': ai_response,
            'saved': True
        })
    
    @action(detail=False, methods=['post'])
    def roast(self, request):
        """
        POST /api/chat/roast/
        
        Get a funny roast of spending habits.
        
        Request body: (empty, no parameters needed)
        {}
        
        Response:
        {
            "roast": "Your food spending is INSANE! ₹2000/month = ..."
        }
        
        Why this endpoint?
        - Users love roasts
        - They screenshot and share
        - Free marketing = more users!
        
        What happens:
        1. Get FinancialAdvisor
        2. Call get_roast() which uses Gemini
        3. Save roast to chat history
        4. Return funny roast
        """
        
        try:
            # Create advisor with user's spending data
            advisor = FinancialAdvisor(request.user)
            # Get funny roast based on their spending
            roast = advisor.get_roast()
        except Exception as e:
            # If Gemini API fails, return error
            return Response(
                {'error': f'Roast failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Save roast to chat history
        # Mark it as '[ROAST MODE]' so frontend can display differently
        ChatMessage.objects.create(
            user=request.user,
            role='assistant',
            message=f"[ROAST MODE] {roast}"
        )
        
        # Return the roast
        return Response({'roast': roast})
    
    @action(detail=False, methods=['post'])
    def savings_plan(self, request):
        """
        POST /api/chat/savings-plan/
        
        Get a plan to achieve savings goal.
        
        Request body:
        {
            "goal_amount": 5000
        }
        
        Response:
        {
            "plan": "To save ₹5000, you need to cut..."
        }
        
        What happens:
        1. User says "I want to save ₹5000"
        2. We tell Gemini the goal
        3. Gemini analyzes their spending
        4. Suggests which categories to cut
        5. Returns actionable plan
        """
        
        # Get the goal amount from request
        goal_amount = request.data.get('goal_amount')
        
        # Check if goal is provided
        if not goal_amount:
            return Response(
                {'error': 'goal_amount required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create advisor with user's data
            advisor = FinancialAdvisor(request.user)
            # Get plan to save this amount
            # NOTE: We haven't built this method yet, but here's the structure
            plan = advisor.get_roast()  # Placeholder for now
        except Exception as e:
            # If Gemini API fails, return error
            return Response(
                {'error': f'Plan failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Return the plan
        return Response({'plan': plan})