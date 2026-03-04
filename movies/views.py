from django.shortcuts import render
from django.http import JsonResponse
from search.views import movie_service

def search_page(request):
    return render(request, "movies/search.html")

def autocomplete(request):
    query = request.GET.get('term', '')
    results = movie_service.autocomplete(query)
    return JsonResponse(results, safe=False)

def movie_detail(request, imdb_id):
    result = movie_service.get_movie_detail(imdb_id)
    if 'error' in result:
        return JsonResponse(result, status=404)
    return JsonResponse(result)
