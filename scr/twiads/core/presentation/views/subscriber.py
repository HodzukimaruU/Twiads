from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from core.business_logic.dto import SubscriberDTO
from core.models import User
from core.business_logic.services import subscribe_user_service, get_followers_service, get_following_service


if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(request_method_list=["GET", "POST"])
def subscriber_controller(request: HttpRequest, username: str) -> HttpResponse:
    subscriber_user = request.user
    
    if request.method == "POST":
        data = SubscriberDTO(username=username, subscriber_username=subscriber_user.username)
        subscribe_user_service(data)
    
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)

@require_http_methods(request_method_list=["GET"])
def followings_controller(request: HttpRequest, username: str) -> HttpResponse:
    following_users = get_following_service(username)
    
    context = {
        "username": username,
        "following_users": following_users,
    }
    
    return render(request=request, template_name='followings.html', context=context)

@require_http_methods(request_method_list=["GET"])
def followers_controller(request: HttpRequest, username: str) -> HttpResponse:
    followers = get_followers_service(username)
    
    context = {
        "username": username,
        "followers": followers,
    }
    
    return render(request=request, template_name='followers.html', context=context)
