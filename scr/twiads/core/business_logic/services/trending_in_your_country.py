from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from core.models import Tweet, User

if TYPE_CHECKING:
    from django.http import HttpRequest


def top_tags_service(user: User) -> QuerySet[Tweet, dict[str, Any]]:
    country = user.country.name if user.country else None
    trending_tags = Tweet.objects.filter(author__country__name=country).values('tags__name').annotate(tag_count=Count('tags')).order_by('-tag_count')[:10]
    return trending_tags
