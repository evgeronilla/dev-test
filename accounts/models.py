import re
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import ugettext_lazy as _
from dev_test.utils import upload_image_path, unique_username_generator
from django.core.validators import MaxValueValidator


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=True, is_staff=False,
                    is_admin=False):
        if not username:
            raise ValueError('Users must have an username')
        else:
            if not re.match("^[a-zA-Z0-9]+$", username):
                raise ValueError("The username may only contain letters and digits")
            username = username.lower()
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            username=username,
        )
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    username        = models.CharField(
                        verbose_name='Username',
                        max_length=150,
                        unique=True, blank=True, null=True,
                        error_messages={'unique': _("A user with that username already exists.")},
                    )
    name            = models.CharField(max_length=100, blank=True, null=True)
    age             = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(150)])
    image           = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    active          = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False)

    timestamp       = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        if app_label == 'account':
            return self.admin
        else:
            return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def owner(self):
        return self


def pre_save_user_receiver(sender, instance, *args, **kwargs):
    if not instance.username:
        instance.username = unique_username_generator(instance)


pre_save.connect(pre_save_user_receiver, sender=User)
