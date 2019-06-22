from rest_framework import serializers
from accounts.models import User


class CatOwnerPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'name',
            'age',
            'image',
        ]
