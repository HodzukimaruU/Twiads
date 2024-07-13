from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

from core.models import User

if TYPE_CHECKING:
    from core.business_logic.dto import SubscriberDTO


def subscribe_user_service(data: SubscriberDTO) -> None:
    user = User.objects.get(username=data.username)
    subscriber_user = User.objects.get(username=data.subscriber_username)
    if subscriber_user not in user.subscriber.all():
        user.subscriber.add(subscriber_user)
        user.subscribers_count += 1
        subscriber_user.subscriptions_count +=1
        user.save()
        subscriber_user.save()
    else:
        user.subscriber.remove(subscriber_user)
        user.subscribers_count -= 1
        subscriber_user.subscriptions_count -=1
        user.save()
        subscriber_user.save()


def get_following_service(username: str) -> QuerySet[User]:
    user = get_object_or_404(User, username=username)
    return user.subscriptions.all()

def get_followers_service(username: str) -> QuerySet[User]:
    user = get_object_or_404(User, username=username)
    return user.subscriber.all()
