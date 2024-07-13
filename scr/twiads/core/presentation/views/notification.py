from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import HttpResponse

from core.business_logic.services import create_like_notification, create_retweet_notification, create_comment_notification, get_user_notifications
from core.models import Like, Retweet, Tweet

if TYPE_CHECKING:
    from django.http import HttpRequest


@login_required
def notification_controller(request: HttpRequest) -> HttpResponse:
    user = request.user
    notifications = get_user_notifications(user)
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications.html', context)

@receiver(post_save, sender=Like)
def like_notification_controller(sender, instance, created, **kwargs) -> None:
    if created:
        create_like_notification(instance)

@receiver(post_save, sender=Retweet)
def retweet_notification_controller(sender, instance, created, **kwargs) -> None:
    if created:
        create_retweet_notification(instance)

@receiver(post_save, sender=Tweet)
def comment_notification_controller(sender, instance, created, **kwargs) -> None:
    if created and instance.parent_tweet is not None:
        create_comment_notification(instance)

