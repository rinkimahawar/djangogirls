from django import forms
from django.db.migrations.state import get_related_models_tuples
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.forms import ModelForm
from .models import Post, User,Comment
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text','category','tag','image','thumbimage')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','country','image','phoneNumber')
        

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']  
           
class EditProfileForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('email','first_name','last_name')

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ('name','email','content')
        
        
