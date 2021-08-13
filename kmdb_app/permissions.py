from rest_framework.permissions import BasePermission
import ipdb

        



class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser and request.user.is_staff

class AllPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user

        
# class CourseSuperUserPermission(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_superuser 

# class CourseStudentPermission(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return not request.user.is_superuser and not request.user.is_staff