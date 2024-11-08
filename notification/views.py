from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
from blogapp.models import Post

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.add(request.user)

    Notification.objects.create(
        sender=request.user,
        recipient=post.author,
        type='like',
        message=f"{request.user.username} liked your post.",
        link=f"/post/{post_id}"
    )
    return redirect('post_detail', post_id=post_id)

def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
  #  notifications = Notification.objects.filter(notification_type='some_type')
    return render(request, 'notifications.html', {'notifications': notifications})

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.link)
