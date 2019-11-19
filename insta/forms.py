from django import forms
from django.forms import ModelForm
from .models import * 
from django.contrib.auth.hashers import check_password



class Registration(ModelForm):
    class Meta:
        model = User
        fields = ['email','full_name','username','password']
        widgets = {
            'email': forms.TextInput(attrs={'class': "form-control form-control-sm"}),
            'full_name': forms.TextInput(attrs={'class': "form-control form-control-sm"}),
            'username': forms.TextInput(attrs={'class': "form-control form-control-sm"}),
            'password': forms.PasswordInput(attrs={'class': "form-control form-control-sm"}),
        }

class Login(forms.Form):
    username = forms.CharField(max_length=50,label='Username')
    password = forms.CharField(widget=forms.PasswordInput())

    widgets = {
        'username':forms.TextInput(attrs={'class': "form-control form-control-sm"}),
        'password':forms.PasswordInput(attrs={'class': "form-control form-control-sm"}),
    }

    def clean_username(self):
        try:
            data = self.cleaned_data['username']
        except KeyError:
            raise forms.ValidationError("Wrong Username.")

        user = User.get_user(data)

        if not user:
            raise forms.ValidationError("Wrong Username.")
        return data
    def clean_password(self):
        data = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
        except:
            raise forms.ValidationError("Wrong Username.")

        user = User.get_user(username)
        if not check_password(data,user.password):
            raise forms.ValidationError("Wrong Password")
        return data

class ProfilePhoto(ModelForm):
    class Meta:
        model = Profile
        exclude = ['bio','user']

class PostPic(ModelForm):
    class Meta:
        model = Image
        exclude = ['profile','likes','posted','user_liked']

 
        
class EditProfile(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user'] 


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['profile','image']
        widgets = {
            'comment':forms.Textarea(attrs={'rows':2, 'cols':55}),
        }

        