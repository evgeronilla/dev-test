from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin


from .views import OwnerViewSet, CatViewSet


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()

owner_router = router.register('owners', OwnerViewSet)

owner_router.register(
    'cats', CatViewSet,
    basename='owner_cat',
    parents_query_lookups=['owner__username'])