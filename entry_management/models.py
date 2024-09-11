# django
from django.db import models
from django.conf import settings

# socket
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Entry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        entry_id = self.id
        message = f'Entry with ID {entry_id} has been deleted.'
        
        # send message to WebSocket group
        async_to_sync(channel_layer.group_send)(
            settings.SOCKET_CHANNEL_NAME,
            {
                'type': 'entry_deleted',
                'message': message,
                'entry_id': entry_id
            }
        )
        
        super().delete(*args, **kwargs)