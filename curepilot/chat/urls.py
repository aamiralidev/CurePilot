from rest_framework.routers import DefaultRouter
from .views import ModelListViewSet, ChatViewSet, chat_completion
from django.urls import path

router = DefaultRouter()
router.register(r'models', ModelListViewSet, basename='model-list')
router.register(r'chat', ChatViewSet, basename='chat')
urlpatterns = router.urls

urlpatterns += [
    path('chat/completion', chat_completion)
]