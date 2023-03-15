from django.contrib.auth import get_user_model
from rest_framework import serializers

from authentication.serializers import UserSerializer

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    password = serializers.CharField()

    def to_representation(self, instance):
       return UserSerializer(instance=instance).data

    def create(self, validated_data):
        user = validated_data["user"]
        user.set_password(validated_data["password"])
        user.save()
        return user