from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile,Image,Comment,Followers,Following,Like
 
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(Followers)
admin.site.register(Like)
