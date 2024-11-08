from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),  # For viewing own profile
    path('profile/<int:user_id>/', views.profile_view, name='profile'),  # For viewing other users' profiles
    path('accounts/register/', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('toggle-follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('users/', views.user_list_view, name='user_list'),
    path('friends/', views.friends_list, name='friends_list'),
    path('friends/<int:friend_id>/post/', views.post_on_friend_profile, name='post_on_friend_profile'),
]
