from rest_framework import generics, mixins

from accounts.models import User
from accounts.api.permissions import IsOwnerOrReadOnly
from cats.api.serializers import CatSerializer, CatDetailSerializer
from cats.api.permissions import IsSameCatBreed
from cats.models import Cat

from .serializers import CatOwnerPublicSerializer


class OwnerAPIListView(generics.ListAPIView):
    queryset            = User.objects.all()
    serializer_class    = CatOwnerPublicSerializer


class OwnerAPIDetailView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes          = [IsOwnerOrReadOnly]
    serializer_class            = CatOwnerPublicSerializer
    queryset                    = User.objects.all()
    lookup_field                = 'username'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OwnerCatAPIListView(generics.ListAPIView):
    serializer_class    = CatSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username", None)

        auth_user_breed_list = Cat.objects.values('breed').distinct().filter(owner=self.request.user)

        return Cat.objects.filter(owner__username=username, breed__in=auth_user_breed_list)


class OwnerCatAPIDetailView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [IsSameCatBreed]
    serializer_class = CatDetailSerializer

    def get_object(self, *args, **kwargs):
        kwargs = self.kwargs
        kw_username = kwargs.get('username')
        kw_name = kwargs.get('name')

        user = User.objects.get(username=kw_username)

        return Cat.objects.get(owner=user, name=kw_name)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


