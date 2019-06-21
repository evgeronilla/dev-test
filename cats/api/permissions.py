from rest_framework import permissions
from accounts.models import User
from cats.models import Cat


class IsSameCatBreed(permissions.BasePermission):
    """
    User can only see cat's detail if the same breed
    """

    message = "Your cat must be the same breed to see this detail."

    # def has_permission(self, request, view):
    #     cat_name = view.kwargs['name']
    #     owner_username = view.kwargs['username']
    #     owner = User.objects.get(username=owner_username)
    #
    #     obj = Cat.objects.get(owner=owner, name=cat_name)
    #     return request.user.cat_set.all().filter(breed=obj.breed).exists()

    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user
