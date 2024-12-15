from rest_framework.permissions import BasePermission

class IsAuthenticatedAdmin(BasePermission):
    """
    Custom permission to allow access only to authenticated users with the 'admin' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'