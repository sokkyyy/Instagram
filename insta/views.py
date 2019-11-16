from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import Registration,Login
from .models import User,Profile,Image
from django.contrib.auth.hashers import make_password,check_password
from django import forms
from django.contrib.auth import login,logout

# Create your views here.
@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')

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

def logout_user(request):
    logout(request)
    return redirect(login_user)


def profile(request, username):
    user = User.get_user(username)
    profile = Profile.get_user_profile(user)
    images = Image.get_profile_images(profile)
    return render(request,'profile.html',{"profile":profile,"images":images})