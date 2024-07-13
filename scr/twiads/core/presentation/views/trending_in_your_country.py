from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from core.business_logic.services import top_tags_service

if TYPE_CHECKING:
    from django.http import HttpRequest


@login_required
@require_http_methods(["GET"])
def top_tags_controller(request: HttpRequest) -> HttpResponse:
    user = request.user
    trending_tags = top_tags_service(user)

    context = {
        'trending_tags': trending_tags,
    }
    return render(request, 'trending_in_your_country.html', context)
