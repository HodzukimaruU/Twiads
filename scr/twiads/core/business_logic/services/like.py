from __future__ import annotations

from django.shortcuts import get_object_or_404
from django.db.models import Count

from core.models import Tweet, User, Like

import logging
    
    
logger = logging.getLogger(__name__)


def like_tweet(tweet_id: int, user: User) -> Tweet:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like_count = tweet.likes_count
    existing_like = Like.objects.filter(tweet=tweet, user=user).first()
    if existing_like:
        existing_like.delete()
        tweet.likes_count = like_count - 1
    else:
        Like.objects.create(tweet=tweet, user=user)
        tweet.likes_count = like_count + 1
    return tweet.save()


def like_comment(comment_id: int, user: User) -> Tweet:
    comment = get_object_or_404(Tweet, id=comment_id)
    like_count = comment.parent_tweet.comments.aggregate(likes_count=Count('likes'))['likes_count']

    existing_like = Like.objects.filter(tweet=comment, user=user).first()
    if existing_like:
        existing_like.delete()
        comment.parent_tweet.likes_count = like_count - 1
    else:
        Like.objects.create(tweet=comment, user=user)
        comment.parent_tweet.likes_count = like_count + 1

    return comment.parent_tweet.save()
