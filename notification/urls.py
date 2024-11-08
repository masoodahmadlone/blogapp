from django.urls import path
#from .views import notification_list, mark_as_read, delete_notification
from . import views 

urlpatterns = [
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notification/<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
]