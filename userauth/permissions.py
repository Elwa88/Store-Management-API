from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.is_superuser

    
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.method == "GET":
            return True
        else:
            return request.user.role == 'admin' or request.user.is_superuser
        
class IsManager(BasePermission):
    def has_permission(self,request,view):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.is_superuser or request.user.role == 'manager'
    
class IsSalesperson(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True