from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import SpendingAnalytics


class AnalyticsViewSet(viewsets.ViewSet):
    """
    Analytics endpoints.
    
    GET /api/analytics/summary/ — Full spending report
    """
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get complete spending summary."""
        days = request.query_params.get('days', 30)
        
        try:
            days = int(days)
        except ValueError:
            days = 30
        
        analytics = SpendingAnalytics(request.user, days=days)
        report = analytics.get_full_report()
        
        return Response(report)