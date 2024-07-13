from __future__ import annotations

from django.shortcuts import get_object_or_404

from core.business_logic.dto import AddCommentDTO
from core.models import Tweet, User

import logging

logger = logging.getLogger(__name__)
    

def add_comment(tweet_id: int, data: AddCommentDTO) -> None:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    Tweet.objects.create(author=data.author, content=data.content, parent_tweet=tweet)
    tweet.comments_count += 1
    tweet.save()


def delete_comment(tweet_id: int,comment_id: int, user : User) -> Tweet:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comment = get_object_or_404(Tweet, id=comment_id, parent_tweet=tweet)
    if comment.author == user:
        comment.delete()
        tweet.comments_count -= 1
        return tweet.save()
        

def comment_list(tweet_id: int) -> [Tweet]:
    comments = Tweet.objects.filter(parent_tweet=tweet_id)
    return comments
