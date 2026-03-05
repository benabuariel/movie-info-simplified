from imdb import Cinemagoer
ia = Cinemagoer()
movies = ia.search_movie('oppenheimer')
for m in movies[:3]:
    print(f"{m['title']} ({m['year']}) -     Rating: {m.get('rating', 'N/A')}")

print(movies)