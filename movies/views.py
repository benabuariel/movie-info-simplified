from django.shortcuts import render
from django.http import JsonResponse
from imdb import Cinemagoer

ia = Cinemagoer()


def search_page(request):
    return render(request, "movies/search.html")


def autocomplete(request):
    query = request.GET.get('term', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)

    try:
        movies = ia.search_movie(query)[:10]  # Top 10 results
        results = []
        for movie in movies:
            ia.update(movie, 'main')  # Get basic info
            results.append({
                'label': f"{movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})",
                'id': movie.movieID,
                'value': movie.get('title', '')
            })
        return JsonResponse(results, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)


def movie_detail(request, imdb_id):
    try:
        movie = ia.get_movie(f'tt{imdb_id}')
        ia.update(movie, info=['main', 'cast', 'plot', 'vote details'])

        # Extract data
        directors = []
        producers = []
        cast = []

        for person in movie.get('cast', [])[:10]:
            name = person.get('name')
            if name:
                cast.append(name)

        for cast_member in movie.get('cast', []):
            role = cast_member.get('role')
            name = cast_member.get('name')
            if name and role:
                if 'director' in role.lower():
                    directors.append(name)
                elif 'producer' in role.lower():
                    producers.append(name)

        result = {
            'title': movie.get('title', 'N/A'),
            'year': movie.get('year', 'N/A'),
            'rating': movie.get('rating', None),
            'rank': movie.get('top 250 rank', 'N/A'),
            'genres': movie.get('genres', []),
            'imdb_url': f"https://www.imdb.com/title/tt{imdb_id}/",
            'cast': cast[:8],
            'directors': directors[:5],
            'producers': producers[:5],
        }
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
