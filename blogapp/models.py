from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from metadata.models import Category, Tag, CookieLog
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=100)
  #  slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  
    content = models.TextField()
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='images/', blank=True, null=True)
    image6 = models.ImageField(upload_to='images/', blank=True, null=True)
    image7 = models.ImageField(upload_to='images/', blank=True, null=True)
  #  image8 = models.ImageField(upload_to='images/', blank=True, null=True)  
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_interactions', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    share_count = models.PositiveIntegerField(default=0)  
    total_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def update_total_likes(self):
        self.total_likes = self.likes.count()  # Directly count the likes
        self.save(update_fields=['total_likes'])

    class Meta:
        ordering = ['-date_posted']  # Order by most recent posts
    
    def total_likes_with_comments(self):
        # Calculate the total likes by summing post likes and likes from comments
        comments_likes_sum = sum(comment.likes.count() for comment in self.comments.all())
        return self.total_likes + comments_likes_sum
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return self.text

    def update_post_likes(self):
        self.post.update_total_likes()

    class Meta:
        ordering = ['-created_at'] 

class Reply(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.author.username}'

    class Meta:
        ordering = ['-created_at'] 


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes', null=True, blank=True)  # Optional
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.post if self.post else self.comment}'

    def clean(self):
        if not self.post and not self.comment:
            raise ValidationError('Like must be associated with either a post or a comment.')
        if self.post and self.comment:
            raise ValidationError('Like cannot be associated with both a post and a comment.')

