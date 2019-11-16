from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
 
class User(AbstractUser):
    full_name = models.CharField(max_length=100,blank=True)

    @classmethod
    def get_user(cls,username):
        try:
            user = cls.objects.get(username=username)
        except ObjectDoesNotExist:
            user = ''
        return user

