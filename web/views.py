from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Page


# Create your views here.
def home(request):
    return render(request, 'home.html')


def normal_results(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        results = Page.objects.filter(
            Q(title__contains=query) | Q(content__contains=query)
        )
        return render(request, 'results.html', {'results': results})
    else:
        return render(request, 'home.html')


def fast_results(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        results = Page.objects.search(query)
        return render(request, 'results.html', {'results': results})
    else:
        return render(request, 'home.html')


def fastest_results(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        # results = Page.objects.annotate(search=SearchVector('title', 'content')).filter(
        #     search=query
        # )
        results = Page.objects.filter(content_search=query)
        return render(request, 'results.html', {'results': results})
    else:
        return render(request, 'home.html')


def details(request, id):
    page = get_object_or_404(Page, pk=id)
    return render(request, 'detail.html', {'page': page})
