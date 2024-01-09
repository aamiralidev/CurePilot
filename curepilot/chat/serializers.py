from rest_framework import serializers
from .models import ModelPermission, ModelCard, ModelList, Chat, ChatResponse

class ModelPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPermission
        fields = '__all__'

class ModelCardSerializer(serializers.ModelSerializer):
    permission = ModelPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = ModelCard
        fields = '__all__'

class ModelListSerializer(serializers.ModelSerializer):
    data = ModelCardSerializer(many=True, read_only=True)

    class Meta:
        model = ModelList
        fields = '__all__'

class ChatResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatResponse
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    chats = ChatResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = '__all__'
