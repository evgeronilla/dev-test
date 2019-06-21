import os
import random

import string

from django.utils.text import slugify


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'

    try:
        username = instance.username
    except:
        from accounts.models import User
        user = User.objects.get(username=instance.username)
        username = user.username

    return f"{username}/{final_filename}"


def upload_cat_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'

    try:
        username = instance.owner.username
    except:
        from accounts.models import User
        user = User.objects.get(username=instance.username)
        username = user.username

    return f"{username}/cat/{final_filename}"


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_username_generator(instance, new_username=None):
    if new_username is not None:
        username = new_username
    else:
        username = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(username=username).exists()
    if qs_exists:
        new_slug = f"{username}-{random_string_generator(size=4)}"
        return unique_username_generator(instance, new_username=new_username)
    return username





