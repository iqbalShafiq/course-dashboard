from django.urls import path
from .views import ConversationView, ConversationStatusView

urlpatterns = [
    path('mcp/conversation/', ConversationView.as_view(), name='mcp-conversation'),
    path('mcp/conversation/<str:conversation_id>/status/', ConversationStatusView.as_view(), name='mcp-conversation-status'),
]