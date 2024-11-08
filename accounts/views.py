from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import ( HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect, HttpResponse, )
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import RegistrationForm, ProfileForm
from .models import Profile, Follow
from blogapp.models import Post
from asgiref.sync import async_to_sync
from blogapp.filters import PostFiltered
from django.contrib.auth import get_user_model
from .models import Friendship

@login_required
def add_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    if request.user == friend:
        messages.error(request, "You cannot add yourself as a friend.")
        return redirect('profile', user_id=user_id)

    friendship, created = Friendship.objects.get_or_create(user=request.user, friend=friend)
    
    if created:
        messages.success(request, f"You are now friends with {friend.username}!")
    else:
        messages.info(request, f"You are already friends with {friend.username}.")
    
    return redirect('profile', user_id=user_id)

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    try:
        friendship = Friendship.objects.get(user=request.user, friend=friend)
        friendship.delete()
        messages.success(request, f"You are no longer friends with {friend.username}.")
    except Friendship.DoesNotExist:
        messages.info(request, f"You are not friends with {friend.username}.")
    
    return redirect('profile', user_id=user_id)

User = get_user_model()

def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not hasattr(user, 'profile'):
                messages.error(request, 'User profile does not exist. Please contact support.')
                return redirect('login')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Suggested Users View
@login_required
def suggested_users(request):
    suggested_users = User.objects.exclude(id=request.user.id)[:5]
    return render(request, 'suggested_users.html', {'suggested_users': suggested_users})

# User List View
class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
  
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

def create_profiles_for_existing_users():
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)

@login_required
def profile_view(request, user_id=None):
    # Fetch the user to follow or the current user
    user_to_follow = get_object_or_404(User, id=user_id) if user_id else request.user
    
    # Get the profile associated with the user
    profile = get_object_or_404(Profile, user=user_to_follow)
    
    # Count followers and followings
    following_count = Follow.objects.filter(follower=user_to_follow).count()
    follower_count = Follow.objects.filter(followed=user_to_follow).count()
    
    # Check if the current user is following the user to follow
    is_following = request.user != user_to_follow and Follow.objects.filter(follower=request.user, followed=user_to_follow).exists()
    
    # Get all posts by the user
    user_posts = user_to_follow.posts.all()

    # Prepare context for rendering
    context = {
        'profile': profile,              # Use the Profile instance
        'following_count': following_count,
        'follower_count': follower_count,
        'user_to_follow': user_to_follow,  # Use this for action URLs
        'is_following': is_following,
        'user_posts': user_posts,
    }
    
    return render(request, 'profile.html', context)  # Ensure correct path for your template
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RegistrationForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)

            # Authenticate user and determine backend
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Assuming your form uses `password1`

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Specify backend: you might have to try either 'django.contrib.auth.backends.ModelBackend'
                # or 'allauth.account.auth_backends.AuthenticationBackend' depending on your setup
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                # Handle failed authentication here
                pass
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    return render(request, 'delete_profile.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def toggle_follow(request, user_id):
    user_to_toggle = get_object_or_404(User, id=user_id)

    # Prevent users from following/unfollowing themselves
    if request.user == user_to_toggle:
        message = 'You cannot follow or unfollow yourself!'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'message': message}, status=400)
        messages.error(request, message)
        return redirect('profile', user_id=user_id)

    # Attempt to get the follow relationship or create it if it doesn't exist
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=user_to_toggle
    )

    if not created:
        # If the relationship existed, delete it to unfollow
        follow.delete()
        is_following = False
        message = 'Unfollowed successfully!'
    else:
        is_following = True
        message = 'Followed successfully!'

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        followers_count = Follow.objects.filter(followed=user_to_toggle).count()
        return JsonResponse({
            'is_following': is_following,
            'followers_count': followers_count,
            'message': message
        })

    # Handle non-AJAX requests
    messages.success(request, message)
    return redirect('profile', user_id=user_id)
def user_list_view(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the logged-in user
    return render(request, 'user_list.html', {'users': users})

@login_required
def friends_list(request):
    friends = request.user.friends.all()  # Get all friends of the logged-in user
    return render(request, 'friends_list.html', {'friends': friends})

@login_required
def post_on_friend_profile(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post.objects.create(user=request.user, content=content)
            # Optionally, you can redirect to the friend's profile or friends list
            return redirect('friends_list')  # Adjust this as necessary

    return render(request, 'post_on_friend_profile.html', {'friend': friend})
