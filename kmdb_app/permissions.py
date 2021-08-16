from rest_framework.permissions import BasePermission
import ipdb


class MovieViewPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser

        if request.method == 'GET':
            return request.user

class ReviewViewPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
            return request.user.is_staff and not request.user.is_superuser

        if request.method == 'GET':
            return request.user.is_staff or request.user.is_superuser

class MovieDetailPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user

        if request.method == 'DELETE':
            return request.user.is_superuser
        

