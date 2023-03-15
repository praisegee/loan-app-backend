from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):

    token = None
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_verified', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ("is_verified", "date_joined")

    def to_representation(self, instance):
        data = super().to_representation(instance)  
        if self.token:
            data["token"] = self.token
        return data

        
    def login(self):
        data = self.data
        errors = {}
        if not data.get("email", None):
            errors["email"] = ["Email is required to login"]
        if not data.get("password", None):
            errors["password"] = ["Password is requred to login"]
        if not errors:
            try:
                user = User.objects.get(email=data.get("email").lower())
                if user.check_password(data.get("password")):
                    token, created = Token.objects.get_or_create(user=user)
                    self.token = token.key
                    data = self.to_representation(user)
                    return data
                errors["password"] = ["Password is incorrect"]
            except User.DoesNotExist:
                errors["email"] = ["Email does not exists"]
        raise serializers.ValidationError(errors)

    def validate(self, data):
        errors = {}

        normalized_email = data.get('email').lower()
        if User.objects.filter(email=normalized_email).exists():
            errors['email'] = ['This Email is already in use']

        try:
            validate_password(password=data.get('password'))
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data
