from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Post
from .models import *
from blog.models import User

class UserSerializers(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        
            
class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    token_detail = serializers.SerializerMethodField("get_token_detail")
    class Meta:
        model = User 
        fields = ('id','email', 'name','username', 'phoneNumber','password', 'image','token_detail')
        extra_kwargs = {
            'token_detail': {'read_only': True},
        }
        
        
    def get_token_detail(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
    
    def get_user(self, request):
            user = request
            return user

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
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
        fields = "__all__"

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name') 


# class SignupSerializer(serializers.Serializer):
#     password = serializers.CharField(style={'input_type': 'password'}, write_only =True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'name', 'password']
#         extra_kwargs ={
#                 'password': {'write_only': True}
#         }

#         def save(self):
#             user=User(
#                 email=self.validated_data['email'],
#                 username=self.validated_data['username'],
#             )
#             print(user, 'QQQQQQQQQQQQQQQQQQQQQQQQQQ')
#             password = self.validated_data['password']
#             confirmpassword = self.validated_data['confirmpassword']
#             if password != confirmpassword:
#                 raise serializers.ValidationError({'password': 'password should be match!!'})  
#             user.set_password(password)
#             user.save()
#             Token.objects.create(user=user)
#             return user
