from django.urls import path
from .views import MovieDetailViewWithAuthentication, MovieView

urlpatterns = [
    path('movies/', MovieView.as_view()),
    path('movies/<int:pk>/', MovieDetailViewWithAuthentication.as_view()),
]