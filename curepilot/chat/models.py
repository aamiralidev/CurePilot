from django.db import models
import uuid
from django.core.validators import MinValueValidator
import time
from django.conf import settings

class ModelPermission(models.Model):
    id = models.CharField(max_length=255, default="modelperm", primary_key=True)
    object = models.CharField(max_length=255, default="model_permission")
    created = models.IntegerField(default=int(time.time()))
    allow_create_engine = models.BooleanField(default=False)
    allow_sampling = models.BooleanField(default=True)
    allow_logprobs = models.BooleanField(default=False)
    allow_search_indices = models.BooleanField(default=False)
    allow_view = models.BooleanField(default=True)
    allow_fine_tuning = models.BooleanField(default=False)
    organization = models.CharField(max_length=255, default="*")
    group = models.CharField(max_length=255, blank=True, null=True)
    is_blocking = models.BooleanField(default=False)

class ModelCard(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    object = models.CharField(max_length=255, default="model")
    created = models.IntegerField(default=int(time.time()))
    owned_by = models.CharField(max_length=255, default="openchat")
    root = models.CharField(max_length=255, blank=True, null=True)
    parent = models.CharField(max_length=255, blank=True, null=True)
    permission = models.ManyToManyField(ModelPermission, blank=True)

class ModelList(models.Model):
    object = models.CharField(max_length=255, default="list")
    data = models.ManyToManyField(ModelCard, blank=True)
    
class Chat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)

class ChatResponse(models.Model):
    conversation_turn = models.IntegerField(validators=[MinValueValidator(1)])
    role = models.CharField(max_length=20)
    content = models.TextField()
    chat_document = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chats')
