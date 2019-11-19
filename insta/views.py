from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import Registration,Login,ProfilePhoto,PostPic,EditProfile,CommentForm,UpdateCaption
from .models import User,Profile,Image,Comment,Followers,Following,Like
from django.contrib.auth.hashers import make_password,check_password
from django import forms
from django.contrib.auth import login,logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .email import send_welcome_email

# Create your views here.
@login_required(login_url='/login') 
def home(request):
    user = request.user
    profile = Profile.get_user_profile(user)
    following = Following.get_user_following(user)
    images_following = Image.get_following_images(following)


    images = Like.has_user_liked(images_following,profile)
    



    return render(request, 'home.html',{"images":images})

def register(request):

    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            #password hashing
            password = form.cleaned_data['password']
            pass_secure = make_password(password)
            #save new user
            user = form.save(commit=False)
            user.password = pass_secure
            
            user.save()

            user_profile = User.get_user(form.cleaned_data['username'])
            profile = Profile(profile_photo='profile_pic/avatar.png', bio="Add a Bio", user=user_profile) 
            profile.save()

            send_welcome_email(user.username,user.email)
            
        return redirect(login_user)
    else:
        form = Registration()

    return render(request,'reg/registration.html',{"form":form})


def login_user(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.get_user(username)
            if check_password(password,user.password):
                login(request,user)
                return redirect(home)      
    else:
        form = Login()

    return render(request,'reg/login.html',{"form":form})

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect(login_user)

@login_required(login_url='/login')
def user_profile(request, username):
    user = User.get_user(username)
    profile = Profile.get_user_profile(user)
    images = Image.get_profile_images(profile)
    
    is_following = Following.is_user_following(request.user, profile)

    comments= Comment.objects.all()

    followers = Followers.get_user_followers(user)

    following = Following.get_user_following(user)    

    if request.method == 'POST':
        photo_form = ProfilePhoto(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.cleaned_data['profile_photo']
            profile.profile_photo = f'profile_pic/{photo}'
            
            profile.save()
            try:
                photo_form.save()
            except IntegrityError:
                return redirect(user_profile, profile.user.username)
    else:
        photo_form = ProfilePhoto()


    return render(request,'profile.html',
    {"profile":profile,"images":images,"comments":comments,
    "followers":followers, "following":following,"photo_form":photo_form,
    "is_following":is_following})
@login_required(login_url='/login') 
def post_pic(request):
    
    if request.method == 'POST':
        form = PostPic(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            
            profile = Profile.get_user_profile(request.user)
            image.profile = profile

            image.save()

            return redirect(user_profile, profile.user.username)
    else:
        form = PostPic()




    return render(request,'post-pic.html',{"form":form})

@login_required(login_url='/login') 
def handle_follow(request,profile_username):

    user_followed = User.get_user(profile_username)
    profile_followed = Profile.get_user_profile(user_followed) 
    following = Following(following=profile_followed,user=request.user)
    following.save()

    user_following = request.user
    profile_following = Profile.get_user_profile(user_following)
    follower = Followers(followers=profile_following,user=user_followed)
    follower.save()


    return redirect(user_profile,profile_username)


@login_required(login_url='/login') 
def handle_unfollow(request,profile_username):
    user_followed = User.get_user(profile_username)
    profile_followed = Profile.get_user_profile(user_followed)

    Following.objects.filter(following=profile_followed,user=request.user).delete()
    
    user_following = request.user
    profile_following = Profile.get_user_profile(user_following)
    Followers.objects.filter(followers=profile_following,user=user_followed).delete()

    
    return redirect(user_profile,profile_username)

@login_required(login_url='/login') 
def handle_like(request,image_id):
    user = request.user
    user_profile = Profile.get_user_profile(user)

    image = Image.objects.get(pk=image_id)
    like_image = Like(user_profile=user_profile,image_liked=image)
    like_image.save()

    image.likes += 1
    image.save()
    return redirect(home)


@login_required(login_url='/login') 
def handle_unlike(request,image_id):
    user = request.user
    user_profile = Profile.get_user_profile(user)

    image = Image.objects.get(pk=image_id)
    Like.objects.filter(user_profile=user_profile,image_liked=image).delete()


    image.likes -= 1
    image.save()
    
    return redirect(home)

@login_required(login_url='/login') 
def handle_like_comment(request,image_id):
    user = request.user
    user_profile = Profile.get_user_profile(user)

    image = Image.objects.get(pk=image_id)
    like_image = Like(user_profile=user_profile,image_liked=image)
    like_image.save()

    image.likes += 1
    image.save()
    return redirect(comment_image,image_id)
@login_required(login_url='/login') 
def handle_unlike_comment(request,image_id):
    user = request.user
    user_profile = Profile.get_user_profile(user)

    image = Image.objects.get(pk=image_id)
    Like.objects.filter(user_profile=user_profile,image_liked=image).delete()


    image.likes -= 1
    image.save()
    
    return redirect(comment_image,image_id)




@login_required(login_url='/login') 
def edit_profile(request):

    user = request.user
    profile = Profile.get_user_profile(user)


    
    if request.method == 'POST':
        edit_form = EditProfile(request.POST, request.FILES)
        if edit_form.is_valid():
            
            profile_pic = edit_form.cleaned_data['profile_photo']
            if profile_pic:
                profile.profile_photo = f'profile_pic/{profile_pic}'
            
            bio = edit_form.cleaned_data['bio']
            if bio:
                profile.bio = bio
            
            profile.save()
            try:
                edit_form.save()
            except IntegrityError:
                return redirect(user_profile, profile.user.username)
    else:
        form = EditProfile()
    return render(request, 'edit_profile.html',
    {"form":form}) 


@login_required(login_url='/login') 
def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')

        images = Image.search_images_caption(search_term)
        
        users = User.search_username(search_term)
        profiles = Profile.get_user_profiles(users)
        return render(request, 'search.html',{'images':images,"profiles":profiles})
    else:
        return render(request, 'search.html')


@login_required(login_url='/login') 
def comment_image(request, image_id):
    find_image = Image.objects.get(pk=image_id)
    
    profile = Profile.get_user_profile(request.user)
    image_liked = Like.has_user_liked([find_image],profile)
    image = image_liked[0]

    
    comments = Comment.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = profile
            comment.image = image

            comment.save()

            return redirect(comment_image, image_id)

    form = CommentForm()
    update_form = UpdateCaption()

    return render(request, 'comment.html',{"image":image,"form":form,"comments":comments,"update_form":update_form,})

@login_required(login_url='/login') 
def update_bio(request,image_id):

    image = Image.objects.get(pk=image_id)
    print(image)
    if request.method == 'POST':
        form = UpdateCaption(request.POST)
        if form.is_valid():
            caption = form.cleaned_data['caption']
            image.update_caption(caption)
            return redirect(comment_image,image_id)


@login_required(login_url='/login') 
def image_delete(request,image_id):
    image = Image.objects.get(pk=image_id)
    image.delete_image()
    return redirect(user_profile, request.user.username)
