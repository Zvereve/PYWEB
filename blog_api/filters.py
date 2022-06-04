from typing import Optional
from django.db.models import QuerySet



def author_id_filter(queryset:QuerySet, author_id:Optional[int]):
    if author_id:
        return queryset.filter(author_id=author_id)
    else:
        return queryset
def public_filter(qeryset:QuerySet, public):
    return qeryset.filter(public=public)

def author__username_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#iexact
    ...


def comment__rating_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#exact
    ...


def comment__rating__gt_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#gt
    ...


def note_create_at__year_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#year
    ...


def note_update_at__month__gte_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#month
    ...