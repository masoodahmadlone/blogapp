from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'actor', 'recipient', 'notification_type', 'timestamp', 'is_read')
    list_filter = ('notification_type', 'is_read', 'timestamp')
    search_fields = ('message', 'actor__username', 'recipient__username')

admin.site.register(Notification, NotificationAdmin)
