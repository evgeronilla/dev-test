from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from accounts.models import User
from accounts.api.permissions import IsOwnerOrReadOnly
from cats.api.serializers import CatSerializer, CatDetailSerializer
from cats.api.permissions import IsSameCatBreed
from cats.models import Cat

from .serializers import CatOwnerPublicSerializer


class OwnerViewSet(NestedViewSetMixin, ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CatOwnerPublicSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class CatViewSet(NestedViewSetMixin, ModelViewSet):
    permission_classes = [IsSameCatBreed]
    serializer_class = CatDetailSerializer
    serializer_action_classes = {
        'list': CatSerializer,
    }
    lookup_field = 'name'

    def get_queryset(self, *args, **kwargs):
        username = self.get_parents_query_dict()['owner__username']
        auth_user_breed_list = Cat.objects.values('breed').distinct().filter(owner=self.request.user)
        return Cat.objects.filter(owner__username=username, breed__in=auth_user_breed_list)

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsSameCatBreed]
        elif self.action == 'create':
            permission_classes = [IsSameCatBreed]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
