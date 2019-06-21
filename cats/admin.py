from django.contrib import admin
from .models import Cat


class CatAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'breed')


admin.site.register(Cat, CatAdmin)
