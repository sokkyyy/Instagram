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


    def __str__(self):
        return f'{self.full_name}'

class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='profile_pic/',blank='True')
    bio = models.TextField(blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    following = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

    @classmethod
    def get_user_profile(cls,user):
        profile = cls.objects.get(user=user)
        return profile

    def __str__(self):
        return f'{self.bio}'
    

class Comment(models.Model):
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.comment}'


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=100,blank=True)
    caption = models.CharField(max_length=100,blank=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    comments = models.ForeignKey(Comment,on_delete=models.CASCADE)
    
    @classmethod
    def get_profile_images(cls,profile):
        images = cls.objects.filter(profile=profile)
        return images


    def __str__(self):
        return f'{self.name}'





