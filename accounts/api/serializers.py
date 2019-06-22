import datetime

from django.core.validators import validate_integer
from django.utils import timezone

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from accounts.models import User

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta                    = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'name',
            'age',
            'image',
            'password',
            'password2',
            'token',
            'expires'
        ]

    def validate(self, data):
        pw  = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def validate_age(self, value):
        validate_integer(value)
        if value < 1:
            raise serializers.ValidationError("Negative value is not accepted.")
        return value

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def create(self, validated_data):
        user_obj = User(name=validated_data.get('name'), age=validated_data.get('age'), image=validated_data.get('image'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
