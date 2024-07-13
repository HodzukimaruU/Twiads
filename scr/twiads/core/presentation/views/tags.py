from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from core.business_logic.services import tags_view_service
from core.presentation.forms import SortForm

from django.http import HttpResponse

if TYPE_CHECKING:
    from django.http import HttpRequest

@login_required
@require_http_methods(["GET"])
def tags_views_controller(request: HttpRequest) -> HttpResponse:
    sort_by = request.GET.get('sort_by', 'Newest')
    tags = request.GET.get('tags')
    tweets = tags_view_service(tags, sort_by)
    form = SortForm(initial={'sort_by': sort_by})
    if tweets:
        page_number = request.GET.get('page', 1)
        paginator = Paginator(tweets, 5)
        page = paginator.get_page(page_number)
        context = {
            'form': form,
            'tweets': page,
            'tags': tags,
        }
        return render(request, 'tags.html', context)
    
    context = {
        'form': form,
        'tweets': None,
        'tags': tags,
    }
    return render(request, 'tags.html', context)

# @login_required
# @require_http_methods(request_method_list=["GET"])
# def home_controller(request: HttpRequest) -> HttpResponse:
#     current_user = request.user
#     page_number = request.GET.get('page', 1)
#     sort_by = request.GET.get('sort_by', 'Newest')
    
#     tweets, retweets, tweets_and_retweets = home_service(current_user, sort_by)
    
#     paginator = Paginator(tweets_and_retweets, 5)
#     page = paginator.get_page(page_number)
    
#     form = SortForm(initial={'sort_by': sort_by})
    
#     context = {
#         'form': form,
#         'tweets': tweets,
#         'retweets': retweets,
#         'tweets_and_retweets': page,
#     }
#     return render(request, 'home.html', context)