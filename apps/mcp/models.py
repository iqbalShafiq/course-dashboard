from django.db import models
from core.models import BaseModel


class Conversation(BaseModel):
    prompt = models.TextField()
    response = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("awaiting_input", "Awaiting Input"),
        ],
        default="pending",
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    context = models.JSONField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='follow_ups')

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Conversation {self.id} - {self.status}"

    def request_information(self, question):
        """Request additional information from the user"""
        self.status = "awaiting_input"
        self.response = question
        self.save()