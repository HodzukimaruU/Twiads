from __future__ import annotations

from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from core.business_logic.services import add_retweet_service, delete_retweet_service

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest
    
    
@login_required
@require_http_methods(request_method_list=["GET"])
def add_retweet_controller(request: HttpRequest, tweet_id) -> HttpResponse:
    user = request.user
    add_retweet_service(tweet_id, user)
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)


@login_required
@require_http_methods(request_method_list=["GET"])
def delete_retweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    user = request.user
    delete_retweet_service(tweet_id=tweet_id, user=user)
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)
 