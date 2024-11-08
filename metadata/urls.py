from django.urls import path
from . import views

urlpatterns = [
    path('all-posts/', views.all_posts, name='all_posts'),
    path('cookies/', views.view_cookies, name='view_cookies'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('collect_cookies/', views.collect_cookie_data, name='collect_cookies'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('tags/', views.tags_list, name='tag_list'), 
    path('tags/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'), 
    path('most-commented/', views.most_commented_posts, name='most_commented_posts'),
    path('most-liked/', views.most_liked_posts, name='most_liked_posts'),
    path('search/', views.search_posts, name='search'),  
    path('search/user/', views.search_user, name='search_user'),
    
]
   