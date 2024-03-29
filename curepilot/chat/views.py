from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ModelList, Chat
from .serializers import ModelListSerializer, ChatSerializer
# from .engine.chat import completion

class ModelListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelList.objects.all()
    serializer_class = ModelListSerializer

class ChatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

@api_view(['POST'])
def chat_completion(request):
    # response = completion(request.data)
    # print(response.count('\t'))
    return Response(request.data['prompt'])