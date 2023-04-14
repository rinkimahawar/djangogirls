from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_view
# from .views import PostView
from .api import *
# from api import PostView


urlpatterns = [
    # Auth APIs
    path('signup_api/', SignupApiView.as_view(), name='signup-api'),
    path('login_api/', LoginApiView.as_view(), name='login-api'),
    path('post_api/', PostApiView.as_view(), name='post_list'),    
    path('postttt_api/', PostApiView.as_view(), name='get_list'),
    path('postdetail_api/<int:pk>/', PostttApiView.as_view(), name='get_detail'),     
    path('comment_api/',CommentApiView.as_view(), name='post-comment'),
    path('commenttt_api/',CommentApiView.as_view(), name='get-comment'),
    path('commentdetail_api/<int:pk>/',CommentdetailApiView.as_view(), name='get-commentdetail'),
    path('category_api/',CategoryApiView.as_view(), name='post-category'),
    path('categoryy_api/',CategoryApiView.as_view(), name='get-category'),        
    path('categorydetail_api/<int:pk>/',CategorydetailApiView.as_view(), name='get-categorydetail'),
    path('tags_api/',TagsApiView.as_view(), name='post-tag'),
    path('tagsdetail/<int:pk>/',TagsdetailApiView.as_view(), name='get-tag'),
    path('tagsss_api/',TagsApiView.as_view(), name='get-tag'),
    path('post-edit-api/<int:id>/',EditpostApiView.as_view(), name='post-edit'),
    path('logout_api/',logoutApiView.as_view(), name='logout'),   
    path('userdetail_api/<int:pk>/', UserdetailApiView.as_view(), name='get_userdetail'),
    path('userlist_api/', UserApiView.as_view(), name='get_userlist'),
    path('userdelete_api/<int:id>/', UserdeleteApiView.as_view(), name='delete-user'),
    path('Tagsdelete_api/<int:id>/', TagsdeleteApiView.as_view(), name='delete-Tags'),
    path('Postdelete_api/<int:id>/', PostdeleteApiView.as_view(), name='delete-Post'),
    path('Commentdelete_api/<int:id>/', CommentdeleteApiView.as_view(), name='delete-Comment'),
    path('Categorydelete_api/<int:id>/', CategorydeleteApiView.as_view(), name='delete-Category'),
]


