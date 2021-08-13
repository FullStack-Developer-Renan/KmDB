from ipdb.__main__ import set_trace
from kmdb_app.models import Genre, Movie, Review
from accounts.serializers import UserDetailSerializer, UserIdSerializer, UserSerializer
from rest_framework import serializers   


class GenrerSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Genre
        fields = ('id','name')   

class ReviewSerializer(serializers.ModelSerializer):
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

    

    
# import ipdb
# from rest_framework import serializers
# from django.shortcuts import get_object_or_404
# from core.models import Account, Customer, Transfer, TransferStatus
# from django.core.exceptions import BadRequest

# from core.services.transfers import account_transfer
  
# class AccountSerializer(serializers.ModelSerializer):
#     # customer = CustomerSerializer()
#     customer_id = serializers.IntegerField(write_only=True)
    
#     class Meta:
#         model = Account
#         fields = '__all__' # Todos os campos da model
#         # fields = ['documentNumber', 'balance']
#         # exclude = ['id']
        
#         # read_only_fields = ('balance',)
        
#         extra_kwargs = {
#             'balance': {'read_only': True}
#         }
        
#         depth = 1
        
#     def create(self, validated_data):
#         # ipdb.set_trace()
#         get_object_or_404(Customer, id=validated_data['customer_id'])
#         # if not Customer.objects.filter(id=validated_data['customer_id']).exists():
#             # raise Exception
            
#         return super().create(validated_data)
    
#     def update(self, instance, validated_data):
#         return super().update(instance, validated_data)


# class AccountNoCustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ['id', 'documentNumber', 'balance']


# class CustomerSerializer(serializers.ModelSerializer):
#     accounts = AccountNoCustomerSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Customer
#         fields = '__all__'
        

# class CustomerNoAccountsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'
    
    
# class TransferSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transfer
#         fields = '__all__'
#         extra_kwargs = {
#             'status': {'read_only': True},
#             'message': {'read_only': True},
#             'created_at': {'read_only': True},
#             'updated_at': {'read_only': True}
#         }
#         depth = 1
        
#     def create(self, validated_data):
#         return account_transfer(**validated_data)