from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow full access to admin users,
    read-only access to others.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_staff or request.user == obj.author)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow full access to the author of an object,
    read-only access to others.
    """

    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_staff or request.user == obj.author)


class IsReaderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to all users.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
