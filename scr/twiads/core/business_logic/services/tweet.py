from __future__ import annotations

from django.shortcuts import get_object_or_404

from core.business_logic.dto import AddTweetDTO, EditTweetDTO

import logging

from core.models import Tweet, Tag, User

logger = logging.getLogger(__name__)


def create_tweet(data: AddTweetDTO) -> None:
    tags: list[str] = data.tags.split("\r\n")
    tags_list: list[Tag] = []
    for tag in tags:
        try:
            tag_from_db = Tag.objects.get(name=tag.lower())
        
        except Tag.DoesNotExist as err:
            logger.warning("Tag does not exist", extra={"Tag": tag}, exc_info=err)
            tag_from_db = Tag.objects.create(name=tag.lower())
            logger.info("Handled error and successfully created tag in db", extra={'tag': tag})
        tags_list.append(tag_from_db)
        
    created_tweet = Tweet.objects.create(author=data.author, content=data.content, parent_tweet=data.parent_tweet)
    created_tweet.tags.set(tags_list)
    if data.parent_tweet:
        replied_tweet = Tweet.objects.get(id=data.parent_tweet)
        replied_tweet.save()
    logger.info("Successfully created tweet", extra={"author":data.author, 'content':data.content, 'parent_tweet':data.parent_tweet})


def get_tweet(tweet_id: int) -> Tweet:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    return tweet


def delete_tweet(tweet_id: int, user : User) -> Tweet:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if tweet.author == user:
        return tweet.delete()


def edit_tweet(data: EditTweetDTO, tweet_id: int) -> None:
    tags: list[str] = data.tags.split("\r\n")
    tags_list: list[Tag] = []
    for tag in tags:
        try:
            tag_from_db = Tag.objects.get(name=tag.lower())
            
        except Tag.DoesNotExist as err:
            logger.warning("Tag does not exist", extra={"Tag": tag}, exc_info=err)
            tag_from_db = Tag.objects.create(name=tag.lower())
            logger.info("Handled error and successfully created tag in db", extra={'tag': tag})
        tags_list.append(tag_from_db)
    tweet = get_object_or_404(Tweet, id=tweet_id)
    tweet.content = data.content
    tweet.tags.clear()
    tweet.tags.set(tags_list)
    tweet.save()
