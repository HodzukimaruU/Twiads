from __future__ import annotations
from typing import Tuple

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Q, QuerySet
from django.core.paginator import Paginator, Page
from django.http import QueryDict

from core.business_logic.dto import EditProfileDto
from core.presentation.forms import SortForm
from core.models import ConfirmationCode, User, Country, Retweet, Tweet
from core.business_logic.services.common import replace_file_name_to_uuid, change_file_size

import uuid
import time

import logging

logger = logging.getLogger(__name__)


def profile_service(user: User, request_get: QueryDict) -> Tuple[QuerySet[Tweet], QuerySet[Retweet], SortForm, Page[Tweet]]:
    tweets = Tweet.objects.filter(Q(author=user), parent_tweet=None)
    retweets = Tweet.objects.prefetch_related('retweets').filter(retweets__user=user)
    tweets_and_retweets = tweets.union(retweets)
    
    form = SortForm(request_get)
    tweets_and_retweets = tweets_and_retweets.order_by('-created_at')
    
    paginator = Paginator(tweets_and_retweets, 5)
    page_number = request_get.get('page', 1)
    page = paginator.get_page(page_number)
    
    return tweets, retweets, form, page


    

def edit_profile(data: EditProfileDto, user: User) -> None:
    if data.avatar:
        data.avatar = replace_file_name_to_uuid(file=data.avatar)
        data.avatar = change_file_size(file=data.avatar)
        user.avatar.delete()
        user.avatar.save(data.avatar.name, data.avatar)
    else:
        user.avatar = data.avatar
        
    country = Country.objects.get(name=data.country)
    User.objects.filter(id=user.id).update(
        username = data.username,
        first_name = data.first_name,
        last_name = data.last_name,
        bio = data.bio,
        email = data.email,
        birth_date = data.birth_date,
        country = country
    )
    
    if data.email != user.email:
        user.email = data.email
        user.is_active = False
        user.save()

        confirmation_code = str(uuid.uuid4())
        code_expiration_time = int(time.time()) + settings.CONFIRMATION_CODE_LIFETIME
        ConfirmationCode.objects.create(code=confirmation_code, user=user, expiration_time=code_expiration_time)

        confirmation_url = settings.SERVER_HOST + reverse("confirm-email") + f"?code={confirmation_code}"
        send_mail(
            subject="Confirm your new email",
            message=f"Please confirm your new email by clicking the link below:\n\n{confirmation_url}",
            from_email=settings.EMAIL_FROM,
            recipient_list=[data.email],
        )
