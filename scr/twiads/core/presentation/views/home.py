from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from core.presentation.forms import SortForm
from core.business_logic.services import home_service

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest



@login_required
@require_http_methods(request_method_list=["GET"])
def home_controller(request: HttpRequest) -> HttpResponse:
    current_user = request.user
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort_by', 'Newest')
    
    tweets, retweets, tweets_and_retweets = home_service(current_user, sort_by)
    
    paginator = Paginator(tweets_and_retweets, 5)
    page = paginator.get_page(page_number)
    
    form = SortForm(initial={'sort_by': sort_by})
    
    context = {
        'form': form,
        'tweets': tweets,
        'retweets': retweets,
        'tweets_and_retweets': page,
    }
    return render(request, 'home.html', context)
