from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from core.business_logic.exceptions import ConfirmationCodeExpired, ConfirmationCodeNotExists
from core.presentation.converters import convert_data_from_form_to_dto
from core.business_logic.services import confirm_user_registration, edit_profile, profile_service
from core.business_logic.dto import EditProfileDto
from core.presentation.forms import EditProfileForm

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


@require_http_methods(request_method_list=["GET"])
def profile_controller(request: HttpRequest) -> HttpResponse:
    current_user = request.user
    tweets, retweets, form, tweets_and_retweets = profile_service(current_user, request.GET)
    context = {"retweets": retweets,
               "form": form,
               "tweets": tweets,
               "tweets_and_retweets": tweets_and_retweets,
               "current_user": current_user
               }
    
    return render(request=request, template_name="profile.html", context=context)


@login_required
@require_http_methods(request_method_list=["GET", "POST"])
def edit_profile_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            initial_data = user.to_dict()
            form = EditProfileForm(initial=initial_data)
            context = {"form": form}
            return render(request=request, template_name="edit_profile.html", context=context)
        else:
            return HttpResponse("You need to log in to edit your profile.")

    elif request.method == "POST":
        if request.user.is_authenticated:
            form = EditProfileForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                data = convert_data_from_form_to_dto(EditProfileDto, data_from_form=form.cleaned_data)
                user = request.user
                if form.cleaned_data["change_email"] == True:
                   edit_profile(data=data, user=user)
                   return redirect(to="confirm-stub")
                else:
                    edit_profile(data=data, user=user)
                    return HttpResponseRedirect(redirect_to=reverse("profile"))
            else:
                form = EditProfileForm(request.POST)
                context = {"form": form}
                return render(request=request, template_name="edit_profile.html", context=context)
            

@require_http_methods(["GET"])
def confirm_email_stub_controller(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Confirmation email sent. Please confirm it by the link.")


@require_http_methods(["GET"])
def registration_confirmation_controller(request: HttpRequest) -> HttpResponse:
    confirmation_code = request.GET["code"]
    try:
        confirm_user_registration(confirmation_code=confirmation_code)
    except ConfirmationCodeNotExists:
        return HttpResponseBadRequest(content="Invalid confirmation code.")
    except ConfirmationCodeExpired:
        return HttpResponseBadRequest(content="Confirmation code expired.")

    return redirect(to="login")
