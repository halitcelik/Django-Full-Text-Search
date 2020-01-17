from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector, SearchVectorField,
                                            TrigramSimilarity)
from django.db import models
from django.urls import reverse

# Create your models here.


search_vectors = (
    SearchVector('title', weight='A')
    + SearchVector('content', weight='B')
    + SearchVector(StringAgg('content', delimiter=' '), weight='D')
)


class PageManager(models.Manager):
    def search(self, text):
        print("using this one")
        search_query = SearchQuery(text)
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('content', text)
        return (
            self.get_queryset()
            .annotate(search=search_vectors)
            .filter(search=search_query)
            .annotate(rank=search_rank + trigram_similarity)
            .order_by('-rank')
        )


class Page(models.Model):
    """docstring for Page"""

    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    content_search = SearchVectorField(null=True, blank=True)
    objects = PageManager()

    class Meta:
        indexes = [GinIndex(fields=["content_search"])]

    def get_absolute_url(self):
        return reverse('web.views.details', args=[str(self.id)])

    def __str__(self):
        return self.title
