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

    def create(self, validated_data):
        user_obj = Cat(
            name=validated_data.get('name'),
            image=validated_data.get('image'),
            breed=validated_data.get('breed'),
            birthdate=validated_data.get('birthdate'),
        )
        user_obj.owner = self.context.get("user")
        user_obj.save()
        return user_obj
