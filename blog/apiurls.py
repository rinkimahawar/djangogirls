from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_view
from blog.api import SignupViewSett,postViewSet,SignupApiView
from blog.api import *
from django.urls import path
# from .views import SignupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'signup', SignupViewSett)
router.register(r'logout', logoutViewSet)
router.register(r'login', loginViewSet)
router.register(r'post', postViewSet)
router.register(r'tags',TagsViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    
]
urlpatterns = [
    # Auth APIs
    path('logout/',logoutViewSet.as_view({'post': 'create'})),
    path('comment/<int:pk>/',CommentViewSet.as_view({'post': 'create'})),
    path('Category/<int:pk>/',CategoryViewSet.as_view({'post': 'create'})),
    path('Tags/<int:pk>/', TagsViewSet.as_view({'post': 'create'})),
    path('login/',loginViewSet.as_view({'post': 'create'})),
    path('post/',postViewSet.as_view({'post': 'create'})),
    path('User/',UserViewSet.as_view({'post': 'create'})),
    path('sign/', SignupViewSett.as_view({'post': 'create'}), name='sign'), 

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


    
# urlpatterns += router.urls
# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# urlpatterns = router.urls

