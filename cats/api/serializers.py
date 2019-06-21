from rest_framework import serializers

from cats.models import Cat


class CatSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cat
        fields = [
            'name',
            'image',
            'uri'
        ]

    def get_uri(self, obj):
        return f'http://127.0.0.1:8000/api/owners/{obj.owner.username}/cats/{obj.name}/'

    def validate(self, data):

        name = data.get('name', None)
        if name == "":
            name = None

        if name is None:
            raise serializers.ValidationError('Name is required.')

        return data


class CatDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = [
            'name',
            'image',
            'breed',
            'birthdate'
        ]

    def validate(self, data):
        name = data.get('name', None)
        if name == "":
            name = None

        if name is None:
            raise serializers.ValidationError('Name is required.')

        return data
