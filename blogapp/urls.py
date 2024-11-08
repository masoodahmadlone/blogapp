from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
 #   path('add-comment/', views.add_comment, name='add_comment'),  
    path('post/<int:post_id>/like/', views.like_post, name='post_like'),
    path('post/<int:post_id>/unlike/', views.post_unlike, name='post_unlike'), 
    path('comment/<int:pk>/like/', views.comment_like, name='comment_like'),
    path('comment/<int:pk>/reply/', views.comment_reply, name='comment_reply'),    
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('create/', views.create_post, name='create_post'),
]
