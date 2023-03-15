from django.contrib import admin
from .models import ForgotPassword


@admin.register(ForgotPassword)
class AdminForgotPassword(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created')