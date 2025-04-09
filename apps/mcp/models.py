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
        ],
        default="pending",
    )
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Conversation {self.id} - {self.status}"