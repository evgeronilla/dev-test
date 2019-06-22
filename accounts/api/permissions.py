from rest_framework import permissions


class AnonPermissionsOnly(permissions.BasePermission):
    """
    Non-authenticated User only
    """

    message = "You are already authenticated. Please logout to register."

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permissions to only allow owners of an object to edit it.
    """

    message = "You must be the owner of this content to change."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
