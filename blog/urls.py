from django.urls import path
from . import views
#from django.conf.urls import patterns, url

app_name = "blog"


urlpatterns = [
    path('signup/',views.signup_request, name="signup"),
    path('',views.post_list, name='post_list'),
    path('post/<slug:slug>',views.post_detail, name='post_detail'),
    path('post_new',views.post_new, name='post_new'),
    path('post_edit/<slug:slug>',views.post_edit, name='post_edit'),
    path("login/",views.login_request, name="login"),
    path("logout/",views.logout_request,name="logout"),
    #path("user",views.profile_view,name="userpage"),
    path('profile/',views.profile_view, name='view_profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('category',views.show_category,name='category'),
    path('tag',views.tag,name='tag'),
]

