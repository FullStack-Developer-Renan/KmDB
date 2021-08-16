from kmdb_app.models import Review
from django.urls import path
from .views import MovieDetailView, MovieView, ReviewView

urlpatterns = [
    path('movies/', MovieView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('movies/<int:pk>/review/', ReviewView.as_view()),
    path('reviews/', ReviewView.as_view()),
]