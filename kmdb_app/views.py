from rest_framework.response import Response
from traitlets.traitlets import All
from kmdb_app.permissions import AdminPermission, AllPermission
from kmdb_app.models import Movie
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from .serializers import MovieDetailSerializer, MovieSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from ipdb import set_trace

class MovieView(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

  
class MovieDetailViewWithAuthentication(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllPermission]

    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer 

    def get(self, request, pk):     
        if request.user.username != '':
            movie = Movie.objects.filter(id=pk).first()
        
            serialized = MovieDetailSerializer(movie)
            return Response(serialized.data)

        movie = Movie.objects.filter(id=pk).first()
    
        serialized = MovieSerializer(movie)
        return Response(serialized.data)





    

  
# from django.db.models import query
# from rest_framework import serializers, status
# from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
# from rest_framework.response import Response
# from .serializer import CustomerSerializer, AccountSerializer, CustomerNoAccountsSerializer, TransferSerializer
# from .models import Customer, Account, Transfer
# import ipdb

# class CustomerView(ListCreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
    

# class CustomerDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

#     def get_serializer(self, *args, **kwargs):
#         method = self.request.method
#         if method == 'PUT' or method == 'PATCH':
#             serializer_class = CustomerNoAccountsSerializer
#         else:
#             serializer_class = self.get_serializer_class()
#         kwargs.setdefault('context', self.get_serializer_context())
#         return serializer_class(*args, **kwargs)

# class AccountView(ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
 

# class AccountDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
    
#     lookup_field = 'id'
    
# class TransferView(ListCreateAPIView):
#     queryset = Transfer.objects.all()
#     serializer_class = TransferSerializer

