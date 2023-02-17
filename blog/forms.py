from django import forms
from django.db.migrations.state import get_related_models_tuples
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import ModelForm
# from .models import UserProfile
from .models import Profile
from .models import Post, User,Comment
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text','category','tags')


class UserForm(forms.ModelForm):
    # password = forms.CharField(Widget= forms.PasswordInput)
    # confirm_Password = forms.CharField(Widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password','city','country','image','gender')
        #fields = '__all__'

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']  
           
class EditProfileForm(ModelForm):
        class Meta:
            model = User
            fields = ('email','first_name','last_name')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        

        fields = ['content','parent']
        
        labels = {
            'content': _(''),
        }
        
        widgets = {
            'content' : forms.TextInput(),
        }
