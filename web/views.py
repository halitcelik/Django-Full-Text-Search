import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Page


# Create your views here.
def home(request):
    return render(request, 'home.html')


@csrf_exempt
def json_result(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        query = json_data['query']
        results = Page.objects.filter(content_search=query)
        json_data = {}
        for item in results.all():
            new_item = {'id': item.id, 'title': item.title}
            json_data[str(item.id)] = new_item
        if len(json_data) > 0:
            return JsonResponse({'json_data': json_data})
        else:
            return JsonResponse({})


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
