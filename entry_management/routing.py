from django.urls import path
from entry_management.consumers import myAsyncJsonConsumer

websocket_urlpatterns=[
    path('ws/', myAsyncJsonConsumer.as_asgi())
]