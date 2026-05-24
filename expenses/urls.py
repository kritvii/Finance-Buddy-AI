from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ExpenseEntryViewSet

# Router automatically creates URLs from ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'expenses', ExpenseEntryViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]


