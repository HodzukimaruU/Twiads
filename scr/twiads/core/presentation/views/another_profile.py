from __future__ import annotations

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.business_logic.services import another_profile_service

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(request_method_list=["GET"])
def another_profile_controller(request: HttpRequest, username: str) -> HttpResponse:
    user, tweets, retweets, form, tweets_and_retweets = another_profile_service(username, request.GET)

  
    context = {
        "user": user,
        "tweets": tweets,
        "retweets": retweets,
        "form": form,
        "tweets_and_retweets": tweets_and_retweets,
    }
    return render(request=request, template_name='another_profile.html', context=context)
