from django.shortcuts import render,get_object_or_404
from django.template.defaultfilters import slugify
from django.shortcuts import redirect, render
from datetime import datetime
from blog.forms import (EditProfileForm)
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from .models import Post, User, Comment,Category
from .forms import UserForm,PostForm,CommentForm
from taggit.models import Tag
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm




def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_list(request):
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'post': post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def signup_request(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "signup successful.")
            return redirect("blog:post_list")
        messages.error(request, "Unsuccessful signup. Invalid information.")
    else:
        form = UserForm()
    return render (request,'blog/signup.html', context={"form":form})       

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("blog:post_list")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="blog/login.html", context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("blog:login")



 #Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
         u_form = UserUpdateForm(instance=request.user)
         p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
         'u_form': u_form,
         'p_form': p_form
     }

    return render(request, 'blog/profile.html', context)

def profile_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request,'blog/view_profile.html', {'User':User}) 

def edit_profile(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=Post)

        if form.is_valid():
            post= form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('blog:view_profile')
    else:
        form = PostForm(instance=request.user)
        return render(request, 'blog/edit_profile.html',{'form': form} )    

def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [ x.slug for x in category_queryset ]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category,slug=slug,parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "postDetail.html", {'instance':instance,'breadcrumbs':breadcrumbs})

    return render(request,"categories.html",{'post_set':parent.post_set.all(),'sub_categories':parent.children.all()})

def home_view(request):
    posts = Post.objects.order_by('-published')
    # Show most common tags 
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }
    return render(request, 'home.html', context)

def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post':post,
    }
    return render(request, 'detail.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'home.html', context)   

def get_context_data(self , **kwargs):
    data = get_context_data(**kwargs)
    connected_comments = Comment.objects.filter(CommentPost=self.get_object())
    number_of_comments = connected_comments.count()
    data['comments'] = connected_comments
    data['no_of_comments'] = number_of_comments
    data['comment_form'] = CommentForm()
    return data

def post(self , request , *args , **kwargs):
    if self.request.method == 'POST':
        print('-------------------------------------------------------------------------------Reached here')
        comment_form = CommentForm(self.request.POST)
    if comment_form.is_valid():
        content = comment_form.cleaned_data['content']
    try:
        parent = comment_form.cleaned_data['parent']
    except:
        parent=None

            

    new_comment = Comment(content=content , author = self.request.user , CommentPost=self.get_object() , parent=parent)
    new_comment.save()
    return redirect(self.request.path_info)