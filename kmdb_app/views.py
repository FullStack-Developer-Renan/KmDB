from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework.response import Response
from traitlets.traitlets import All
from kmdb_app.permissions import MovieDetailPermission, MovieViewPermission, ReviewViewPermission
from kmdb_app.models import Movie, Review
from rest_framework import request, serializers
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from .serializers import MovieDetailSerializer, MovieSerializer, ReviewDetailSerializer, ReviewSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from ipdb import set_trace


class MovieView(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [MovieViewPermission]
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    def get(self, request, *args, **kwargs):

        if request.data != {}:
            movie = Movie.objects.filter(title__contains=request.data['title']).all()

            return Response(MovieSerializer(movie, many=True).data)

        return super().get(request, *args, **kwargs)
  
class MovieDetailView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [MovieDetailPermission]

    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer 
    
    def get_serializer(self, *args, **kwargs):
        
        if self.request.user.username != '':
            serializer_class = MovieDetailSerializer
 
        else:
            serializer_class = MovieSerializer
            
        return serializer_class(*args, **kwargs)

class ReviewView(ListCreateAPIView, UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewViewPermission]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):

        get_object_or_404(Movie, id=kwargs['pk'])

        if Review.objects.filter(critic=request.user, movie=Movie.objects.filter(id=kwargs['pk']).first()).exists():
            return Response({"detail": "You already made this review."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if request.data['stars'] > 10:
            return Response({"stars": ["Ensure this value is less than or equal to 10."]}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data['stars'] < 1:
            return Response({"stars": ["Ensure this value is greater than or equal to 1."]}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(**request.data, critic=request.user, movie=Movie.objects.filter(id=kwargs['pk']).first())
        
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

    def get_serializer(self, *args, **kwargs):

        if self.request.user.is_superuser == True and self.request.user.is_staff == True:
            serializer_class = ReviewDetailSerializer

        elif self.request.user.is_superuser == False and self.request.user.is_staff == True:
            review =  Review.objects.filter(critic_id=self.request.user.id).all()

            return Response(ReviewDetailSerializer(review, many=True).data)

        return serializer_class(*args, **kwargs)

    def update(self, request, *args, **kwargs):

        review = get_object_or_404(Review, movie_id=kwargs['pk'], critic_id=request.user.id)
        
        review.stars = request.data['stars']
        review.review = request.data['review']
        review.spoilers = request.data['spoilers']

        review.save()

        return Response(ReviewSerializer(review).data)

