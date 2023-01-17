from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserObjectManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("User have to have an email address ")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email,  password)
        user.is_superuser = True
        user.is_staff = True

        user.save()	
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, 
        unique=True, 
        verbose_name="Email Address"
    )
    username = models.CharField(max_length=200)
    is_employee = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_email_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)


    objects = UserObjectManager()


    def get_email(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
