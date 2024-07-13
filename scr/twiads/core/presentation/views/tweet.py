from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from core.business_logic.services import create_tweet, edit_tweet, get_tweet, comment_list, delete_tweet
from core.presentation.converters import convert_data_from_form_to_dto
from core.business_logic.dto import AddTweetDTO, EditTweetDTO
from core.presentation.forms import AddTweetForm, EditTweetForm

import logging

if TYPE_CHECKING:
    from django.http import HttpRequest
    
    
logger = logging.getLogger(__name__)


@login_required
@require_http_methods(request_method_list=["GET", "POST"])
def add_tweet_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddTweetForm()
        context = {"form": form}
        logger.info("Rendered form")
        return render(request=request, template_name="add_tweet.html", context=context)
    
    elif request.method == "POST":
        form = AddTweetForm(data=request.POST)
        if form.is_valid():
            logger.info("Form is valid")
            data = convert_data_from_form_to_dto(AddTweetDTO, data_from_form=form.cleaned_data)
            data.author = request.user
            create_tweet(data=data)
            return HttpResponseRedirect(redirect_to=reverse("home"))
        else:
            logger.info("Invalid form", extra={"post_data": request.POST})
    context = {"form": form}
    return render(request, "add_tweet.html", context=context)


@login_required
@require_http_methods(request_method_list=['GET'])
def get_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    tweet = get_tweet(tweet_id=tweet_id)
    comments = comment_list(tweet_id=tweet_id)
    context = {"tweet": tweet, "comments": comments}
    return render(request=request, template_name="get_tweet.html", context=context)


@login_required
@require_http_methods(request_method_list=['POST'])
def delete_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    user = request.user
    delete_tweet(tweet_id=tweet_id, user=user)
    return redirect('profile')    


@login_required
@require_http_methods(request_method_list=["GET", "POST"])
def edit_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    if request.method == "GET":
        form = EditTweetForm()
        context = {"form": form}
        logger.info("Rendered form")
        return render(request=request, template_name="edit_tweet.html", context=context)
    elif request.method == "POST":
        form = EditTweetForm(data=request.POST)
        if form.is_valid():
            logger.info("Form is valid")      
            data = convert_data_from_form_to_dto(EditTweetDTO, data_from_form=form.cleaned_data)
            edit_tweet(data=data, tweet_id=tweet_id)
            return redirect('get-tweet', tweet_id)
        else:
            logger.info("Invalid form", extra={"post_data": request.POST})

    context = {"form": form}
    return render(request, "edit_tweet.html", context=context) 
