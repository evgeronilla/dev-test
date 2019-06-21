from django.conf.urls import url
from django.urls import path

from .views import OwnerCatAPIListView, OwnerCatAPIDetailView


urlpatterns = [
    # path('', OwnerAPIListView.as_view(), name='owner-list'),
    # path('<slug:username>/', OwnerAPIDetailView.as_view(), name='owner-details'),
    path('<slug:username>/cats/', OwnerCatAPIListView.as_view(), name='cat-list'),
    path('<slug:username>/cats/<slug:name>/', OwnerCatAPIDetailView.as_view(), name='cat-detail'),
]
