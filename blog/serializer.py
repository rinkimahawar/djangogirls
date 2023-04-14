from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Post
from .models import *



class UserSerializer(serializers.ModelSerializer):
    """ user serializer """

    token_detail = serializers.SerializerMethodField("get_token_detail")
    class Meta:
        model = User 
        fields = ('id','email', 'name','username', 'phoneNumber', 'image','token_detail')
        extra_kwargs = {
            'token_detail': {'read_only': True},
        }
        
        
    def get_token_detail(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
    
    def get_user(self, request):
            user = request
            return user
    
 
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text','user') 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'content','email', 'post') 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name') 

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name') 


