from django.db import models
from django.conf import settings
from dev_test.utils import upload_cat_image


class Cat(models.Model):
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    name        = models.CharField(verbose_name='Name', max_length=255, null=True, blank=True)
    breed       = models.CharField(verbose_name='Breed', choices=settings.CAT_BREED_LIST, max_length=150, blank=True, null=True)
    birthdate   = models.DateField(verbose_name='Birth Date', blank=True, null=True)
    image       = models.ImageField(verbose_name='Picture', upload_to=upload_cat_image, blank=True, null=True)

    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
