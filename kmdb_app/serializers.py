from django.contrib.auth.models import User
from ipdb.__main__ import set_trace
from rest_framework.generics import get_object_or_404
from kmdb_app.models import Genre, Movie, Review
from accounts.serializers import UserReviewSerializer, UserSerializer
from rest_framework import serializers   


class GenrerSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Genre
        fields = ('id','name')   

class ReviewSerializer(serializers.ModelSerializer):

    critic = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        exclude = ('movie',) 

class ReviewDetailSerializer(serializers.ModelSerializer):

    critic = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):

    genres = GenrerSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__' 

    def create(self, validated_data):  

        genres = validated_data.pop('genres')

        movie = Movie.objects.create(**validated_data) 

        genre_list = []

        for genre in genres:
            genre = Genre.objects.get_or_create(**genre)[0]

            genre_list.append(genre)

        movie.genres.set(genre_list)

        return movie

class MovieDetailSerializer(serializers.ModelSerializer):

    genres = GenrerSerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__' 

class MovieIdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('id') 
