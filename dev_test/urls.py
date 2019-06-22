from django.contrib import admin
from django.urls import path, include
from accounts.api.cat_owner.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api.urls')),
    path('api/', include(router.urls)),
]
