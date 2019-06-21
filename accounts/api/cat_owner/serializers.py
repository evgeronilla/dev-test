from rest_framework import serializers
from accounts.models import User


class CatOwnerPublicSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'name',
            'age',
            'image',
            'uri'
        ]

    def get_uri(self, obj):
        return f'http://127.0.0.1:8000/api/owners/{obj.username}/'
