from django.shortcuts import render,get_object_or_404
from django.template.defaultfilters import slugify
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from .models import Post, User,Category,Tags
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    print(comments)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try :
                parent = request.POST.get('comment_id')
                parent = Comment.objects.filter(id = parent).last()
                print(parent, 'parent instanceeeee')
            except:
                parent=None
            comments = form.save(commit=False)
            comments.post = post
            comments.parent = parent
            comments.save()
        return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comments}) 
    

def post_list(request):
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'post': post})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.tag.set(form.cleaned_data.get('tag'))
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
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
	return redirect("blog:login")


def profile_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request,'blog/view_profile.html', context) 


def edit_profile(request, slug):
    post=get_object_or_404(Post, slug=slug)
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


def show_category(request, slug):
    post = Post.objects.filter(post, slug=slug)
    request_category = Category.objects.get(slug=slug)
    categories = Category.objects.all()
    tags = Tags.objects.all()
    
    return render(request,'blog/categories.html',{'post':post,'category':request_category,'categories':categories,'tags':tags, })

def tag(request,slug):
    post = Post.objects.filter(post, slug=slug)
    request_tag = Tags.objects.get(slug=slug)
    # print(request_tag,"qqqqqqqqqqqqqqqqqqqqqqqqqqq")
    categories =Category.objects.all()
    tags = Tags.objects.all()
    # print(tags,"eeeeeeeeeeeeeeeeeeeeeeeeeeeee")

    return render (request, 'blog/tag.html', {'post':post,'tag':request_tag,'categories':categories,'tags':tags,})


