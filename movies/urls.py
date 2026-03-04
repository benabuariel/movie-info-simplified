from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_page, name="search_page"),
    path("autocomplete/", views.autocomplete, name="autocomplete"),
    path("movie/<str:imdb_id>/", views.movie_detail, name="movie_detail"),
]
