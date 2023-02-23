from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from django_extensions.db.fields import AutoSlugField
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from PIL import Image

class User(AbstractUser):
    email = models.EmailField(max_length=44,null=True,blank=True)
    city = models.CharField(max_length=23)
    country = models.CharField(max_length=16)
    phoneNumber = models.CharField(default=0, max_length=16)
    image = models.ImageField(upload_to='Profile_picture', null=True, blank=True)

    def __str__(self):
         return self.email
 

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name',unique=True)
    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=40)
    slug = AutoSlugField(populate_from='name',unique=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tags)
    slug = AutoSlugField(populate_from='title',unique=True)
    image = models.ImageField(upload_to='image/')
    thumbimage = models.ImageField(upload_to='thumbimage/')


    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    content = models.TextField()
    date_posted = models.DateTimeField(default=now)
    email = models.EmailField(max_length=44,null=True,blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        return self.name

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False           