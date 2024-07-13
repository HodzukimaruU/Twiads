from __future__ import annotations

from core.models import NotificationType, Notification, Like, Retweet, Tweet, User

from typing import List


def get_user_notifications(user: User) -> List[Notification]:
    return user.notifications.order_by('-created_at')


def create_like_notification(like: Like) -> None:
    tweet: Tweet = like.tweet
    author: User = tweet.author
    tweet_url: str = f"/tweet/{tweet.id}/"
    notification_text: str = f"User {like.user.username} liked your tweet: {tweet.content}"
    notification_type: NotificationType = NotificationType.objects.get(name="likes")
    notification: Notification = Notification.objects.create(text=notification_text, notification_type=notification_type)
    notification.user.set([author])


def create_retweet_notification(retweet: Retweet) -> None:
    tweet: Tweet = retweet.tweet
    author: User = tweet.author
    tweet_url: str = f"/tweet/{tweet.id}/"
    notification_text: str = f"User {retweet.user.username} retweeted your tweet: {tweet.content}"
    notification_type: NotificationType = NotificationType.objects.get(name="retweets")
    notification: Notification = Notification.objects.create(text=notification_text, notification_type=notification_type)
    notification.user.set([author])


def create_comment_notification(comment: Tweet) -> None:
    tweet: Tweet = comment.parent_tweet
    author: User = tweet.author
    tweet_url: str = f"/tweet/{tweet.id}/"
    notification_text: str = f"User {comment.author.username} commented your tweet: {tweet.content}"
    notification_type: NotificationType = NotificationType.objects.get(name="replies")
    notification: Notification = Notification.objects.create(text=notification_text, notification_type=notification_type)
    notification.user.set([author])