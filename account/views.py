import random
import string

from django.contrib.auth import get_user_model
from rest_framework import decorators, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from account.emails import Email
from authentication.serializers import UserSerializer as s

from .models import ForgotPassword

User = get_user_model()


class AuthenticationViewSet(viewsets.GenericViewSet):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = s.UserSerializer
        
    @decorators.action(methods=["POST"], detail=False, url_path="forgot-password")
    def forgot_password(self, request):
        """
        Create a reset code and send it to users email
        ---------------
        `
            sample_request = {
                "email":"email@example.com"
            }
        `
        """
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            otp = ''.join(random.choices(string.digits, k=6))
            ForgotPassword.objects.update_or_create(user=user, defaults={"otp":otp})
            #send email with otp
            Email(
                subject="Loan App - Reset Password", 
                receiver=email, 
                plain_message=f'Your Reset code is: {otp}',
                template='email/reset_password.html', 
                data={"otp_code":otp}
            ).send()
        except User.DoesNotExist:
            return Response({"message":"User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"A mail containing your reset link has been sent to your email"})
    

    @decorators.action(methods=["POST"], detail=False, url_path="change-password")
    def change_password(self, request):
        """
        Change password for authenticated user
        --------------------------------------
        `
            sample_request = {
                "password":"password"
            }
        `
        """
        if not request.user.is_authenticated:
            return Response({"message": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        password = request.data.get("password", None)
        if not password:
            return Response({"message": "Password is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        self.request.user.set_password(password)
        self.request.user.save()
        return Response({"message":"Your password has been reset"})
        

    @decorators.action(methods=["POST"], detail=False, url_path="reset-password")
    def reset_password(self, request):
        """
        reset password
        ---------------
        `
            sample_request = {
                "email":"email@example.com",
                "otp": "123456"
                "password":"password"
            }
        `
        """
        email = request.data.get("email")
        otp = request.data.get("otp") 
        password =  request.data.get("password")
        try:
            user = User.objects.get(email=email)
            otp_obj = ForgotPassword.objects.get(user=user, otp=otp)
            if not password:
                return Response({"message": "Password is invalid"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            otp_obj.delete()
        except User.DoesNotExist:
            return Response({"message":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except ForgotPassword.DoesNotExist:
            return Response({"message":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Your password has been reset successfully"})