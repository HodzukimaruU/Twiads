from __future__ import annotations

from core.models import Tweet


def tags_view_service(tags: str, sort_by: str) -> Tweet:
    tweets = Tweet.objects.all()

    if tags:
        tweets = tweets.filter(tags__name__icontains=tags)

    if sort_by == 'Newest':
        tweets = tweets.order_by('-created_at')
    elif sort_by == 'Likes':
        tweets = tweets.order_by('-likes_count')

    return tweets
