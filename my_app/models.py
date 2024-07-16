from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self,name,email,phone_number,password=None,**extra_fields):
        user = self.model(name=name,email=email,phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,name,email,phone_number,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user(name,email,phone_number,password,**extra_fields)


# Create your models here.
class Users(AbstractUser):
    username = None
    name = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10,unique=True, blank=True, null=True)
    otp = models.CharField(max_length=4, blank=True,null=True)
    otp_duration = models.DateTimeField(null=True,blank=True)
    max_otp_try = models.IntegerField(default=3)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['phone_number','email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} {self.email} {self.phone_number}'

    # def is_otp_valid(self):
    #     if self.otp_duration:
    #         return timezone.now() < self.otp_duration + timedelta(minutes=3)
    #     return False


