from django.shortcuts import render
from django.http import JsonResponse

def search_page(request):
    return render(request, "movies/search.html")

def autocomplete(request):
    q = request.GET.get("term", "")  # jQuery UI uses "term"
    # TODO: search IMDb here and build a list of {label, value, id}
    results = [
        # example format
        {"label": "The Matrix (1999)", "value": "The Matrix", "id": "tt0133093"},
    ]
    return JsonResponse(results, safe=False)

def movie_detail(request, imdb_id):
    # TODO: fetch movie details by imdb_id from IMDb
    movie = {
        "title": "The Matrix",
        "year": 1999,
        "rating": 8.7,
        "rank": 16,
        "directors": ["Lana Wachowski", "Lilly Wachowski"],
        "producers": ["Joel Silver"],
        "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
    }
    return JsonResponse(movie)
