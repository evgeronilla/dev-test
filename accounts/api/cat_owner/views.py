
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.response import Response

from accounts.models import User
from accounts.api.permissions import IsOwnerOrReadOnly
from cats.api.serializers import CatSerializer, CatDetailSerializer
from cats.api.permissions import IsSameCatBreed
from cats.models import Cat

from .serializers import CatOwnerPublicSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = CatOwnerPublicSerializer
    lookup_field = 'username'


class OwnerCatViewSet(viewsets.ViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = [IsSameCatBreed]
    serializer_class = CatDetailSerializer, CatSerializer
    lookup_field = 'name'

    def list(self, request, username_username=None):

        auth_user_breed_list = Cat.objects.values('breed').distinct().filter(owner=self.request.user)

        queryset = Cat.objects.filter(owner__username=username_username, breed__in=auth_user_breed_list)

        serializer = CatSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, name=None, username_username=None):
        user = User.objects.get(username=username_username)

        queryset = Cat.objects.get(owner=user, name=name)

        serializer = CatDetailSerializer(queryset)
        return Response(serializer.data)


    # def get_object(self, *args, **kwargs):
    #     kwargs = self.kwargs
    #     kw_username = kwargs.get('username')
    #     kw_name = kwargs.get('name')
    #
    #     user = User.objects.get(username=kw_username)
    #
    #     return Cat.objects.get(owner=user, name=kw_name)

    # def get_queryset(self):
    #     kw_username = self.kwargs['username_username']
    #     print(kw_username)
    #
    #     user = User.objects.get(username=kw_username)
    #
    #     return Cat.objects.filter(owner=user)


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


