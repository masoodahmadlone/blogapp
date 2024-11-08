from django.urls import re_path
from .consumers import NotificationConsumer  # Ensure the import is correct

# Define websocket_urlpatterns
websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),  
]
