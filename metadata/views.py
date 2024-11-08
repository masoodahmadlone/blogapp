from django.shortcuts import render
from .models import Category, Tag, CookieLog
from blogapp.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blogapp.filters import PostFiltered
from django.db.models import Count, Q
# Create your views here.
@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # Use 'categories' instead of 'category' to match the ManyToManyField
    posts = Post.objects.filter(categories=category)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'category_posts.html', context)

@login_required
def posts_by_tag(request, tag_slug):
    """View to display posts filtered by tag."""
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'posts_by_tag.html', {'tag': tag, 'posts': posts})

def tags_list(request):
    tags = Tag.objects.all()  # Retrieve all tags
    return render(request, 'tags_list.html', {'tags': tags})

def view_cookies(request):
    cookies = CookieLog.objects.all()
    return render(request, 'view_cookies.html', {'cookies': cookies})

def cookie_policy(request):
    return render(request, 'cookie_policy.html')

def collect_cookie_data(request):
    cookies = request.COOKIES
    for name, value in cookies.items():
        CookieLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            cookie_name=name,
            cookie_value=value
        )
    return HttpResponse("Cookie data collected.")

def some_view(request):
    cookies_accepted = request.COOKIES.get('cookie_consent')
    return render(request, 'some_template.html', {'cookies_accepted': cookies_accepted})


@login_required
def search_posts(request):
    """Search functionality for posts."""
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    return render(request, 'search_results.html', {'results': results, 'query': query})

@login_required
def search_user(request):
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = []
    return render(request, 'search_user.html', {'users': users})

@login_required
def filter_posts(request):
    filtered_posts = PostFiltered(request.GET, queryset=Post.objects.all())
    return render(request, 'filter_posts.html', {'filter': filtered_posts})

@login_required
def most_commented_posts(request):
    m_posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')
    return render(request, 'most_commented_posts.html', {'m_posts': m_posts})

@login_required
def most_liked_posts(request):
    l_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    return render(request, 'most_liked_posts.html', {'l_posts': l_posts})

@login_required
def all_posts(request):
    posts = Post.objects.select_related('author').prefetch_related('likes').order_by('-date_posted')
    return render(request, 'all_posts.html', {'posts': posts})
