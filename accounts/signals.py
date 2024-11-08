from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    user.profile.is_online = False
    user.profile.save()
