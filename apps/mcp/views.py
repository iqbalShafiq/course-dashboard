from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from .models import Conversation, Analysis
from .services import MCPService
from huey.contrib.djhuey import task
from core.views import LoginRequiredMixinView

@task()
def process_conversation(conversation_id):
    service = MCPService()
    print(f"Processing conversation with ID: {conversation_id}")
    return service.process_prompt(conversation_id)

@task()
def process_analysis(analysis_id):
    service = MCPService()
    print(f"Processing analysis with ID: {analysis_id}")
    return service.process_analysis(analysis_id)

class ConversationView(LoginRequiredMixinView, View):
    def post(self, request):
        prompt = request.POST.get('prompt')
        parent_id = request.POST.get('parent_id')
        additional_context = request.POST.get('context')
        
        if not prompt:
            return JsonResponse({"error": "Prompt is required"}, status=400)
            
        conversation = Conversation.objects.create(
            prompt=prompt,
            actor=request.user
        )

        # Link to parent conversation if this is a follow-up
        if parent_id:
            try:
                parent = Conversation.objects.get(id=parent_id)
                conversation.parent = parent
                conversation.context = parent.context or []
            except Conversation.DoesNotExist:
                pass

        # Add new context if provided
        if additional_context:
            try:
                context_data = conversation.context or []
                context_data.append(additional_context)
                conversation.context = context_data
            except Exception as e:
                print(f"Error adding context: {str(e)}")

        conversation.save()
        
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
                "error": conversation.error,
                "requires_input": conversation.status == "awaiting_input"
            })
        except Conversation.DoesNotExist:
            return JsonResponse({"error": "Conversation not found"}, status=404)

class AnalysisListView(LoginRequiredMixinView, ListView):
    model = Analysis
    template_name = "analysis_list.html"
    context_object_name = "analyses"

class AnalysisDetailView(LoginRequiredMixinView, DetailView):
    model = Analysis
    template_name = "analysis_detail.html"
    context_object_name = "analysis"

class CreateAnalysisView(LoginRequiredMixinView, View):
    def post(self, request):
        prompt = request.POST.get('prompt')
        visualization = request.POST.get('visualization_type', 'table')
        
        # Create analysis object
        analysis = Analysis.objects.create(
            title=f"Analysis: {prompt[:50]}...",
            query=prompt,
            visualization_type=visualization,
            actor=request.user
        )
        
        # Process asynchronously
        process_analysis(analysis.id)
        
        return JsonResponse({"id": analysis.id, "status": "processing"})

    def get(self, request):
        # Handle GET request by redirecting to analysis list
        return redirect('analysis-list')