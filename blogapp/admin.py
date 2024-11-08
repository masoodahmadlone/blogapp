from django.contrib import admin
from blogapp.models import Post, Comment, Like, Category, Tag, CookieLog


@admin.register(CookieLog)
class CookieLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'cookie_name', 'cookie_value', 'timestamp')
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
