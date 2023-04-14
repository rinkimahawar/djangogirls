from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout
from rest_framework import status as tstatus
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializer import UserSerializer, PostSerializer,CommentSerializer,CategorySerializer,TagsSerializer




class SignupApiView(APIView):
    """ API for signup """

    permission_classes = [AllowAny]

    def post(self, request):
        """ post method for signup api """
        res = {}
        # try:
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        cpassword = request.POST.get("cpassword", None)
        name = request.POST.get('name', None)		

        if email is None:
            res['status'] = False
            res['message'] = "Email is Required"
            res['data'] = []
            return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            res['status'] = False
            res['message'] = "Account already exist with this Email"
            res['data'] = []
            return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
        
        if name is None:
            res['status'] = False
            res['message'] = "Name is Required"
            res['data'] = []
            return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

        if password is None or password != cpassword:
            res['status'] = False
            res['message'] = "Password not Match!"
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

        data = request.data
        try:
            data._mutable = True
        except:
            pass
            data['username'] = email
            data['status'] = 'Active'

        serializer = UserSerializer(
            data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res_data = serializer.data
            user = User.objects.filter(id=res_data['id']).last()
            user.set_password(password)
            user.save()


            name = str(user.name)
            recipient_list = [user.email]
            
            res['status'] = True
            res['message'] = "You've registered successfully"
            res['data'] = res_data
            return Response(res, status=tstatus.HTTP_200_OK)
            
        else:
            res['status'] = False
            error = next(iter(serializer.errors))
            res['message'] = serializer.errors[str(error)][0]
            res['data'] = res_data
            return Response(res, status=tstatus.HTTP_200_OK)
  

        """ API for login """
class LoginApiView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        """ post method for login api """
        res = {}
        try:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)

            if username is None:
                res['status'] = False
                res['message'] = "username is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

            if password is None:
                res['status'] = False
                res['message'] = "Password is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)
            if user is None:
                res['status'] = False
                res['message'] = "Invalid Email or Password!"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST) 
            else:
                
                serializer = UserSerializer(user, read_only=True, context={'request': request})
                if serializer :
                    res['status'] = True
                    res['message'] = "Authenticated successfully"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid Email or Password!!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        

        
class PostApiView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        res = {}
        try:
            text = request.data.get("text", None)			
            title = request.data.get("title", None)

            if text is None:
                res['status'] = False
                res['message'] = "text is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

            if title is None:
                res['status'] = False
                res['message'] = "title is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            
            data = request.data
            try:
                data._mutable = True
            except:
                pass
            data['user'] = request.user.id
                
            if data:
                serializer = PostSerializer(data=data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res['status'] = True
                    res['message'] = "post created successfully"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid text or  title!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        
# class PostApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        try:
            post = Post.objects.all()
            print(post,'pppppppppp')

            if post is None:
                res['status'] = False
                res['message'] = "post is not found"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

                
            if post:
                serializer = PostSerializer(post, many=True,read_only=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "post get list successfully"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "post fetch unsuccessfully"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        
class PostttApiView(APIView):       

    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        res = {}
        post = None
        try:
            post = Post.objects.filter(pk=pk).all()

            if post is None:
                res['status'] = False
                res['message'] = "post is not found"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
            if post:
                serializer = PostSerializer(post, many=True,read_only=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "post get successfully"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "post fetch unsuccessfully"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            else:
                    res['status'] = False
                    res['message'] = "there is no post for this id!!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)    
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST) 
         

class PostdeleteApiView(APIView):  
    def delete(self, request, id=None):
        post = Post.objects.get(id=id)
        post.delete()
        return Response({"message": "Post deleted successfully."},status=tstatus.HTTP_400_BAD_REQUEST)       
                          

       
        

class CommentApiView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        res = {}
        try:
            name = request.data.get('name', None)
            email = request.data.get("email", None)
            content = request.data.get("content", None)
            post_id = request.data.get("post", None)

            if email is None:
                res['status'] = False
                res['message'] = "Email is Required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

            user = User.objects.filter(email=email).last()
            if user is None:
                res['status'] = False
                res['message'] = "Account not found"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)
        
            if name is None:
                res['status'] = False
                res['message'] = "Name is Required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)

            if content is None:
                res['status'] = False
                res['message'] = "content is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            
            if post_id is None:
                res['status'] = False
                res['message'] = "post is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            
            if post_id:
                post =Post.objects.filter(id=post_id).last()

            if post is None:
                res['status'] = False
                res['message'] = "Post not found"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                    
            data = request.data
            try:
                data._mutable = True
            except:
                pass
            data['user'] = user.id
            data['post'] = post.id
                
            if data:
                serializer = CommentSerializer(data=data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res['status'] = True
                    res['message'] = "Comment successfully"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid name  or  email or content"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        

    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        try: 
            cat = Comment.objects.all()
            print(cat, 'AAAAAAAAAAAAA')      
 
        
            if cat is None:
                res['status'] = False
                res['message'] = "empty Comment"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)            
        
            if cat:
                serializer = CommentSerializer(cat, read_only=True, many=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "all Comment here"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid Comment"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)  

class CommentdetailApiView(APIView):            
            
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        res = {}
        comment = None
        try: 
            comment = Comment.objects.get(pk=pk)       
        
            if comment is None:
                res['status'] = False
                res['message'] = "empty Comment"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)            
        
            if comment:
                serializer = CommentSerializer(comment, read_only=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "all Comment here"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid Comment"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            else:
                    res['status'] = False
                    res['message'] = "there is no comment available!!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                        
                    
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)             
        
class CommentdeleteApiView(APIView):  
    def delete(self, request, id=None):
        comment = Comment.objects.get(id=id)
        comment.delete()
        return Response({"message": "Comment deleted successfully."},status=tstatus.HTTP_400_BAD_REQUEST)       
                    
        

class CategoryApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        try: 
            cat = Category.objects.all()
            print(cat, 'AAAAAAAAAAAAA')      
 
        
            if cat is None:
                res['status'] = False
                res['message'] = "empty category"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)            
        
            if cat:
                serializer = CategorySerializer(cat, read_only=True, many=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "all category here"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid name"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)  

    def post(self, request):
        res = {}
        # try:
        name = request.data.get('name', None)           
        
        user = User.objects.filter(id=request.user.id).last()   
    
        if name is None:
            res['status'] = False
            res['message'] = "Name is Required"
            res['data'] = []
            return Response(res, status=tstatus.HTTP_404_NOT_FOUND)            
    
        data = request.data
        try:
            data._mutable = True
        except:
            pass
        data['user'] = user.id
            
        if data:
            serializer = CategorySerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                res['status'] = True
                res['message'] = "Category successfully post"
                res['data'] = serializer.data
                return Response(res, status=tstatus.HTTP_200_OK)
            else:
                res['status'] = False
                res['message'] = "Invalid name"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            
class CategorydetailApiView(APIView):            
            
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        res = {}
        cat =None
        try: 
            cat = Category.objects.get(pk=pk)      
        
            if cat is None:
                res['status'] = False
                res['message'] = "empty category"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)            
        
            if cat:
                serializer = CategorySerializer(cat, read_only=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "all category here"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid name"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            else:
                    res['status'] = False
                    res['message'] = "there is no category for this id!!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)    
                    
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST) 
        
class CategorydeleteApiView(APIView):  
    def delete(self, request, id=None):
        category = User.objects.get(id=id)
        category.delete()
        return Response({"message": "Category deleted successfully."},status=tstatus.HTTP_400_BAD_REQUEST)       
                    



    

class TagsApiView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        res = {}
        try:
            name = request.POST.get('name', None)            
        
            if name is None:
                res['status'] = False
                res['message'] = "Name is Required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND) 

            user = User.objects.filter(id=request.user.id).last()              
        
            data = request.data
            try:
                data._mutable = True
            except:
                pass
            data['user'] = user.id
                
            if data:
                serializer = TagsSerializer(data, read_only=True, context={'request': request})
                if serializer :
                    res['status'] = True
                    res['message'] = "Tags successfully post"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid name"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        
# class TagsApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        try:
            # name = request.POST.get('name', None) 
            tags = Tags.objects.all() 
            print(tags,'ttttttttttttttt')          
        
            if tags is None:
                res['status'] = False
                res['message'] = "empty tags"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)            
        
            
                
            if tags:
                serializer = TagsSerializer(tags, read_only=True, many=True,context={'request': request})
                if serializer :
                    res['status'] = True
                    res['message'] = "All Tags here"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid name"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

    permission_classes = [IsAuthenticated]

class TagsdetailApiView(APIView):  

    def get(self, request,pk):
        res = {}
        tags = None
        try:
            tags = Tags.objects.get(pk=pk)           
        
            if tags is None:
                res['status'] = False
                res['message'] = "empty tags"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_404_NOT_FOUND)            
                                   
            if tags:
                serializer = TagsSerializer(tags, read_only=True,context={'request': request})
                if serializer :
                    res['status'] = True
                    res['message'] = " Tags here"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "Invalid tag"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            else:
                    res['status'] = False
                    res['message'] = "there is no tag for this id!!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)    
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST) 

class TagsdeleteApiView(APIView):  
    def delete(self, request, id=None):
        tags = Tags.objects.get(id=id)
        tags.delete()
        return Response({"message": "Tags deleted successfully."},status=tstatus.HTTP_400_BAD_REQUEST)       
            

        

        
class EditpostApiView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        res = {}
        post = None
        try:
            text = request.data.get("text", None)
            title = request.data.get("title", None)

            if text is None:
                res['status'] = False
                res['message'] = "text is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)

            if title is None:
                res['status'] = False
                res['message'] = "title is required"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            
            post =Post.objects.filter(id=id).last()
            if post is None:
                res['status'] = False
                res['message'] = "Post not found!!"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            
            data = request.data
            try:
                data._mutable = True
            except:
                pass
            data['user'] = request.user.id
            if data:
                serializer = PostSerializer(data=data, instance=post)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res['status'] = True
                    res['message'] = "post edit successfully"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    error = next(iter(serializer.errors))
                    res['message'] = serializer.errors[str(error)][0]
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            else:
                res['status'] = False
                res['message'] = "Something went wrong!"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        
        

class logoutApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        res={}
        # try:
        user = User.objects.filter(id=request.user.id).last()
        request.user.auth_token.delete()

        logout(request)
        serializer = UserSerializer(user, read_only=True, context={'request':request})
        res['status'] = True
        res['message'] = "logout successfully"
        res['data'] = serializer.data
        return Response(res, status=tstatus.HTTP_200_OK)
    

class UserdetailApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        res = {}
        user = None
        try:
            user = User.objects.get(pk=pk)

            if user is None:
                res['status'] = False
                res['message'] = "user is not found"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
            if user:
                serializer = UserSerializer(user,read_only=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "user detail get successfully"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "user detail fetch unsuccessfully"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
            else:
                    res['status'] = False
                    res['message'] = "there is no user available!!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST) 
        
class UserApiView(APIView):  
    permission_classes = [IsAuthenticated]
      

    def get(self, request):
        res = {}
        try:
            user = User.objects.all()

            if user is None:
                res['status'] = False
                res['message'] = "user is not found"
                res['data'] = []
                return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
            if user:
                serializer = UserSerializer(user, many=True,read_only=True, context={'request': request})
                if serializer:
                    res['status'] = True
                    res['message'] = "user get list successfully!!"
                    res['data'] = serializer.data
                    return Response(res, status=tstatus.HTTP_200_OK)
                else:
                    res['status'] = False
                    res['message'] = "user list not fetch!!"
                    res['data'] = []
                    return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=tstatus.HTTP_400_BAD_REQUEST)
        
class UserdeleteApiView(APIView):  
    def delete(self, request, id=None):
        user = User.objects.get(id=id)
        user.delete()
        return Response({"message": "User deleted successfully."},status=tstatus.HTTP_400_BAD_REQUEST)       
            


    
        


        


        