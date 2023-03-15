from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication import serializers as s

from account.emails import Email


class LoginAPI(views.APIView):
    """
    Login Api
    """
    serializer_class = s.UserSerializer
    permission_classes = [AllowAny]
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title="Login API", 
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='string'),
        },
        required=["email", "password"]
    )
    user_response = openapi.Response('Response description', 
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title="Response", 
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, description='User id'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                'verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Email verification status'),
                'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Date Joined'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token')
        })
    )

    @swagger_auto_schema(request_body=request_body, responses={200: user_response})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        data = serializer.login()
        return Response(data, status=status.HTTP_200_OK)


class RegisterAPI(views.APIView):
    """
    Register Api
    """
    serializer_class = s.UserSerializer
    permission_classes = [AllowAny]
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title="Register API", 
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, format='username', description='string'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, format='firstname', description='string'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, format='lastname', description='string'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='string'),
        },
        required=['username', 'first_name', 'last_name', "email", "password"]
    )
    user_response = openapi.Response('Response description', 
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title="Response", 
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT64, description='User id'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                'verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Email verification status'),
                'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Date Joined'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token')
        })
    )

    @swagger_auto_schema(request_body=request_body, responses={200: user_response})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        print(new_user.email)
        Email(receiver=str(new_user.email), template='email/welcome_verify.html', plain_message="Welcome", data={'username': str(new_user.username)}).send()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
