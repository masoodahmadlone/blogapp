from django import template

register = template.Library()

@register.filter
def is_following(user, followed_user):
    return user.following.filter(followed=followed_user).exists()
