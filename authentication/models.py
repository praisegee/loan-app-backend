from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext as _


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a Auth with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(_("Username"), unique=True, max_length=150, null=True, blank=True)
    email = models.EmailField(_("Email"), unique=True, max_length=255)
    is_verified = models.BooleanField(_("Verified"), default=False, 
        help_text="Boolean field to check if user's email has been verified")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.get_full_name()
