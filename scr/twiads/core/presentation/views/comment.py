from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from core.models import Tweet
from core.presentation.converters import convert_data_from_form_to_dto
from core.business_logic.services import add_comment, get_tweet, delete_comment
from core.business_logic.dto import AddCommentDTO
from core.presentation.forms import AddCommentForm
import logging



if TYPE_CHECKING:
    from django.http import HttpRequest
    
    
logger = logging.getLogger(__name__)


@login_required
@require_http_methods(request_method_list=["POST"])
def add_comment_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    tweet = get_tweet(tweet_id=tweet_id)
    if request.method == "POST":
        form = AddCommentForm(data=request.POST)
        if form.is_valid():
            data = convert_data_from_form_to_dto(AddCommentDTO, data_from_form=form.cleaned_data)
            data.author = request.user
            add_comment(tweet_id=tweet_id, data=data)
            return HttpResponseRedirect(redirect_to=reverse("get-tweet", args=[tweet_id]))
    else:
        logger.info("Invalid form", extra={"post_data": request.POST})

    context = {"form": form, "tweet": tweet}
    return render(request=request, template_name="comment.html", context=context)


@login_required
@require_http_methods(request_method_list=["POST"])
def delete_comment_controller(request: HttpRequest, tweet_id, comment_id: int) -> HttpResponse:
    user = request.user
    delete_comment(user=user, tweet_id=tweet_id, comment_id=comment_id)
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)

