from __future__ import annotations

from typing import Tuple

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import QueryDict
from django.db.models.query import QuerySet
from django.core.paginator import Page

from core.models import User, Tweet, Retweet
from core.presentation.forms import SortForm



def another_profile_service(username: str, request_get: QueryDict) -> Tuple[User, QuerySet[Tweet], QuerySet[Retweet], SortForm, Page[Tweet]]:
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(Q(author=user), parent_tweet=None)
    retweets = Tweet.objects.prefetch_related('retweets').filter(retweets__user=user)
    
    tweets_and_retweets = tweets.union(retweets)
    
    form  = SortForm(request_get)
    tweets_and_retweets = tweets_and_retweets.order_by('-created_at')
    
    paginator = Paginator(tweets_and_retweets, 5)
    page_number = request_get.get('page', 1)
    page = paginator.get_page(page_number)
  
    return user, tweets, retweets, form, page
