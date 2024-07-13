from typing import List, Tuple

from django.db.models import Q

from core.models import Tweet
from core.models import User



def home_service(user: User, sort_by: str) -> Tuple[List[Tweet], List[Tweet], List[Tweet]]:
    followed_users = user.subscriptions.all()
    
    tweets = Tweet.objects.filter(Q(author=user) | Q(author__in=followed_users), parent_tweet=None)
    retweets = Tweet.objects.prefetch_related('retweets').filter(retweets__user__in=followed_users)
    
    tweets_and_retweets = tweets.union(retweets)
    
    if sort_by == 'Newest':
        tweets_and_retweets = tweets_and_retweets.order_by('-created_at')
    elif sort_by == 'Likes':
        tweets_and_retweets = tweets_and_retweets.order_by('-likes_count')
    
    return tweets, retweets, tweets_and_retweets

