from rest_framework import serializers

from .models import Profile


class UserPrivateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = [
            "username",
            "bio",
            "picture",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = [
            "username",
            "bio",
            "picture",
            # "posts",
        ]
