

# Create your models here.
""" Database Model """


from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)



class UserManager(BaseUserManager):
    
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    # fields that we want to use 
    # phone_number = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active =models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = UserManager()
    # if want to login form password from phone_number then use 
    # USERMANE_FIELDS = ['phone_number']
    USERNAME_FIELD = 'email'