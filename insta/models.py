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
    
    @classmethod
    def search_username(cls,search_term):
        users = cls.objects.filter(username__icontains = search_term)
        return users     

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


    @classmethod
    def get_user_profile(cls,user):
        try:
            profile = cls.objects.get(user=user)
        except ObjectDoesNotExist:
            return None
        return profile
    @classmethod
    def get_user_profiles(cls,users):
        profiles = []
        for user in users:
            profile = cls.get_user_profile(user)
            if profile == None:
                continue
            profiles.append(profile)
        return profiles

    def __str__(self):
        return f'{self.bio}'
    




class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=100,blank=True)
    caption = models.CharField(max_length=100,blank=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    posted = models.DateTimeField(auto_now_add=True)
    user_liked = models.BooleanField(default=False)
    

    
    @classmethod
    def get_profile_images(cls,profile):
        images = cls.objects.filter(profile=profile)
        return images

    @classmethod
    def get_following_images(cls,profiles):
        images = []
        for profile in profiles:
            image = cls.get_profile_images(profile.following)

            if image:
                for img in image:
                    images.append(img)
        return images

    @classmethod
    def search_images_caption(cls,search_term):
        images = cls.objects.filter(caption__icontains = search_term)
        return images 

    def __str__(self):
        return f'{self.name}'




class Comment(models.Model):
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)

    


    def __str__(self):
        return f'{self.comment}'
    
    
class Followers(models.Model):
    
    followers = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_followers')
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    @classmethod
    def get_user_followers(cls,user):
        followers = cls.objects.filter(user=user)
        return followers



    def __unicode__(self):
        return f'{self.user}'

class Following(models.Model):
    following = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_following')
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    @classmethod
    def get_user_following(cls,user):
        following = cls.objects.filter(user=user)
        return following
    
    @classmethod
    def is_user_following(cls,user,profile):
        if cls.objects.filter(following=profile,user=user):
            return True
        else:
            return False

    
    def __unicode__(self):
        return f'{self.user}'

class Like(models.Model):
    user_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    image_liked = models.ForeignKey(Image, on_delete=models.CASCADE)

    @classmethod
    def has_user_liked(cls,images,profile):
        for image in images:
            if cls.objects.filter(user_profile=profile,image_liked=image):
                image.user_liked = True
            else:
                image.user_liked = False
        return images

    def __unicode__(self):
        return f'{self.image_liked}' 