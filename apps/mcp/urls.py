from django.urls import path
from .views import (
    ConversationView, 
    ConversationStatusView,
    AnalysisListView,
    AnalysisDetailView,
    CreateAnalysisView
)

urlpatterns = [
    path('mcp/conversation/', ConversationView.as_view(), name='mcp-conversation'),
    path('mcp/conversation/<str:conversation_id>/status/', ConversationStatusView.as_view(), name='mcp-conversation-status'),
    path('analysis/', AnalysisListView.as_view(), name='analysis-list'),
    path('analysis/create/', CreateAnalysisView.as_view(), name='create-analysis'),
    path('analysis/<str:pk>/', AnalysisDetailView.as_view(), name='analysis-detail'),
]