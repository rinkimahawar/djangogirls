from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth import get_user_model
from PIL import Image

class User(AbstractUser):
    email = models.EmailField(max_length=44,null=True,blank=True)
    city = models.CharField(max_length=23)
    country = models.CharField(max_length=16)
    gender = models.CharField(max_length=25)
    image = models.ImageField(upload_to='Profile_picture', null=True, blank=True)

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phoneNumber = models.IntegerField(default=0)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image
            # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image
    def __str__(self):
         return self.user.username


    #def createProfile(sender, **kwargs):
    #   if kwargs['created']:
    #        profile = Profile.objects.created(user=kwargs['instance'])

     #   post_save.connect(createProfile, sender=User)       

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    def __str__(self):
        return self.name


class Post(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    # publish = models.DateField(auto_now=False,auto_now_add=False,)
    # slug = models.SlugField(unique=True)
    Tags = TaggableManager()


    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category # for now ignore this instance method
        
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]       

class PublishingUser(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Blog(models.Model):
    published_date_time= models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200 , unique=True)
    #slug = models.SlugField(max_length=200 , unique=True)
    author = models.ForeignKey(PublishingUser, on_delete= models.CASCADE , related_name='blog_posts')
    description = models.CharField(max_length=300, null=True)
    content = models.TextField()
    Tags= TaggableManager()
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    name = models.CharField(max_length=40)
    slug = AutoSlugField(populate_from='name',unique=True)
    def __str__(self):
        return self.name


class Comment(models.Model):
    CommentPost = models.ForeignKey(Blog , on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()