from django.http import JsonResponse
from django.views import View
from .models import Conversation
from .services import MCPService
from huey.contrib.djhuey import task
from core.views import LoginRequiredMixinView

@task()
def process_conversation(conversation_id):
    service = MCPService()
    print(f"Processing conversation with ID: {conversation_id}")
    return service.process_prompt(conversation_id)

class ConversationView(LoginRequiredMixinView, View):
    def post(self, request):
        prompt = request.POST.get('prompt')
        
        if not prompt:
            return JsonResponse({"error": "Prompt is required"}, status=400)
            
        conversation = Conversation.objects.create(
            prompt=prompt,
            actor=request.user
        )
        
        # Process asynchronously
        process_conversation(conversation.id)
        
        return JsonResponse({
            "id": conversation.id,
            "status": conversation.status
        })
    
class ConversationStatusView(LoginRequiredMixinView, View):
    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            return JsonResponse({
                "status": conversation.status,
                "response": conversation.response,
                "error": conversation.error
            })
        except Conversation.DoesNotExist:
            return JsonResponse({"error": "Conversation not found"}, status=404)