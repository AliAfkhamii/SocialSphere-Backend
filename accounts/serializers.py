from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            User.USERNAME_FIELD,
            'password'
        ]

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        : param value: password of a user
        : return: a hashed version of the password
        """
        return make_password(value)
