from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User 
from .models import Post, Comment, Like
from notification.models import Notification
from .forms import CommentForm, PostForm
from accounts.models import Profile, Follow, create_user_profile
from django.contrib import messages
User = get_user_model()
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post
from accounts.models import Profile, Follow
from notification.models import Notification
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType

@login_required
def home(request):
    # Existing querysets and logic
    h_posts = Post.objects.select_related('author').prefetch_related('comments', 'likes').order_by('-date_posted')[:20]
    m_posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')
    suggested_users = Profile.objects.exclude(user=request.user).prefetch_related('user')
    cookies_accepted = request.COOKIES.get('cookie_consent') == 'true'
    
    form = CommentForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, pk=request.POST.get('post_pk'))
        comment.author = request.user
        comment.save()

        # Create a notification for the post author
        if comment.post.author != request.user:
            Notification.objects.create(
             #   actor=request.user,
                recipient=comment.post.author,
                content_type=ContentType.objects.get_for_model(Comment),  # Use the correct content type
                object_id=comment.id,  # Use the comment ID
                notification_type='comment'
            )
        return redirect('home')

    profile = get_object_or_404(Profile, user=request.user) if request.user.is_authenticated else None
    
    for user in suggested_users:
        user.is_following = request.user.following.filter(followed=user.user).exists()

    return render(request, 'home.html', {
        'h_posts': h_posts,
        'm_posts': m_posts,
        'comment_form': form,
        'suggested_users': suggested_users,
        'cookies_accepted': cookies_accepted,
        'profile': profile,  
    })

@login_required
def create_post(request):
    # Log the user and their authentication status
    print("User:", request.user)
    print("Is authenticated:", request.user.is_authenticated)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the logged-in user to the post
            post.save()  # Now save to the database
            messages.success(request, "Post created successfully!")  # Add success message
            return redirect('home')  # Redirect after successful creation
    else:
        form = PostForm()
        
    return render(request, 'create_post.html', {'form': form})


def get_parent_comments(post):
    parent_comments = Comment.objects.filter(post=post, parent_comment=None)
    nested_comments = get_nested_comments(parent_comments)  # Build nested structure
    return nested_comments

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = get_parent_comments(post)

    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text')
            parent_comment_id = request.POST.get('parent_comment')
            parent_comment = Comment.objects.get(pk=parent_comment_id) if parent_comment_id != '0' else None

            new_comment = Comment.objects.create(
                post=post,
                author=request.user,
                text=text,
                parent_comment=parent_comment
            )
            return redirect('post_detail', pk=pk)  

    image_urls = []
    for field in ["image1", "image2", "image3", "image4", "image5", "image6", "image7"]:
        image = getattr(post, field)
        if image:
            image_urls.append(image.url)

    comment_form = CommentForm()  

    context = {
        'post': post,
        'comments': comments,  
        'comment_form': comment_form,  
        'image_urls': image_urls,  
    }
    return render(request, 'post_detail.html', context)


def get_nested_comments(comments):
    nested_comments = []
    for comment in comments:
        replies = Comment.objects.filter(parent_comment=comment)  
        nested_comments.append({
            'comment': comment,
            'replies': get_nested_comments(replies)  
        })
    return nested_comments



@login_required
def comment_like(request, pk):
    # Check if user is authenticated (this is redundant with @login_required)
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You need to be logged in to like a comment.'}, status=403)

    # Get the comment by its primary key (pk)
    comment = get_object_or_404(Comment, pk=pk)

    # Attempt to create or get an existing like object for the user on this comment
    like, created = Like.objects.get_or_create(comment=comment, user=request.user)

    # If the like already exists, delete it (indicating an "unlike" action)
    if not created:
        like.delete()

    # Recalculate the total likes for the post that this comment is associated with
    post = comment.post
    if hasattr(post, 'total_likes') and not callable(post.total_likes):
        # If total_likes is a field, use it directly
        post_likes_count = post.total_likes
    else:
        # If total_likes is a method, call it to get the latest count
        post_likes_count = post.total_likes()

    # Return a JSON response with whether it was liked and the new total like count
    return JsonResponse({
        'liked': created,
        'total_likes': post_likes_count
    })

def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)

    # Update the total likes including comment likes
    total_likes = post.total_likes()

    next_url = request.GET.get('next', post.get_absolute_url())
    return JsonResponse({'total_likes': total_likes, 'next': next_url})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    post.update_total_likes()  
    return redirect('home')

@login_required
def post_unlike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        post.update_total_likes()  # Update total likes after unlike
    return redirect('home')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
        return redirect('profile')
    return HttpResponseForbidden("You don't have permission to delete this post.")

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def comment_reply(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = parent_comment.post
            reply.parent_comment = parent_comment
            reply.author = request.user
            reply.save()
            # Change this line to match your URL pattern
            return redirect('post_detail', post_id=parent_comment.post.pk)  # Use post_id instead of pk
    else:
        form = CommentForm()
    return render(request, 'comment_reply.html', {'parent_comment': parent_comment, 'form': form})


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)  # Unlike the comment
    else:
        comment.likes.add(request.user)  # Like the comment

    return redirect('post_detail', post_id=comment.post.id)  