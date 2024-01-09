from rest_framework import viewsets
from .models import ModelList, Chat
from .serializers import ModelListSerializer, ChatSerializer

class ModelListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelList.objects.all()
    serializer_class = ModelListSerializer

class ChatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
