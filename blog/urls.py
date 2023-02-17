from django.urls import path
from .views import *
#from django.conf.urls import patterns, url

app_name = "blog"


urlpatterns = [
    path('signup/', signup_request, name="signup"),
    path('',post_list, name='post_list'),
    path('post/<int:pk>', post_detail, name='post_detail'),
    path('post_new', post_new, name='post_new'),
    path('post_edit/<int:pk>', post_edit, name='post_edit'),
    path("login/",login_request, name="login"),
    path("logout/",logout_request,name="logout"),
    #path("user",views.profile_view,name="userpage"),
    path('profile/', profile_view, name='view_profile'),
    path('editprofile/',edit_profile,name='editprofile'),
    path('category',show_category,name='category'),
]

