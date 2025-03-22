from django.contrib.auth.models import User
from django.db import models

from core.utils import generate_id


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, default=generate_id, editable=False, max_length=24)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
