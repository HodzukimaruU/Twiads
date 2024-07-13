from __future__ import annotations

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from core.business_logic.services import like_tweet, like_comment

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


@login_required
@require_http_methods(request_method_list=["GET"])
def like_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    user = request.user
    like_tweet(user=user, tweet_id=tweet_id)
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)


@login_required
@require_http_methods(request_method_list=["GET"])
def like_comment_controller(request: HttpRequest, comment_id: int) -> HttpResponse:
    user = request.user
    like_comment(user=user, comment_id=comment_id)
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)
