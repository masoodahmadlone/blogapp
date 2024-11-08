from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('friend_request', 'Friend Request'),
    )

    actor = models.ForeignKey(User, related_name='notifications_sent', on_delete=models.CASCADE, default=1)
    recipient = models.ForeignKey(User, related_name='notifications_received', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='like')
    message = models.TextField(blank=True)
    link = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor.username} -> {self.recipient.username}: {self.notification_type}"

    class Meta:
        ordering = ['-timestamp']  # Optional: To order notifications by timestamp descending
