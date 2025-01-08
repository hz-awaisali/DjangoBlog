from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from markdown import markdown


#home module
# @login_required(login_url='/login/')
def home(request):
    posts = Blog.objects.all()
    for post in posts:
        post.body_html = markdown(post.body)
    return render(request, 'home.html', {'posts': posts})


#detailed blog module
# @login_required(login_url='/login/')
def detailed_blog(request, bid):
    post = Blog.objects.get(id=bid)
    # categories = Blog.objects.values_list('category', flat=True).distinct()
    content_html = markdown(post.body)
    return render(request, 'detailed_blog.html', {'post': post, 'content_html': content_html})


#user registeration module
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken')
            return redirect('/register/')
        else:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            user.set_password(password)
            user.save()
            messages.info(request, 'User created successfully')
            return redirect('/login/')
    return render(request, 'auth/register_page.html')



#login module
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'auth/login_page.html')


#logout module
@login_required(login_url='/login/')

def logout_user(request):
    logout(request)
    return redirect('/login/')


#blog creation module
@login_required(login_url='/login/')

def create_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        image = request.FILES.get("image")
        category = request.POST.get("category")
        author = request.user.first_name + " " + request.user.last_name
        content = request.POST.get("content")
        
        # Save the blog to the database
        blog = Blog.objects.create(
                title=title,
                body=content,
                image=image,
                category=category,
                author=author)
        blog.save()
        messages.success(request, "Blog created successfully")
        return redirect("/create/")

    return render(request, "create_blog.html")


#update blogs list module
@login_required(login_url='/login/')

def update_blogs_list(request):
    blogs = Blog.objects.filter(author=request.user.first_name + " " + request.user.last_name)
    return render(request, 'update_blogs_list.html', {'blogs': blogs})


#update blog module
@login_required(login_url='/login/')

def update_blog(request, bid):
    blog = Blog.objects.get(id=bid)
    if request.method == "POST":
        blog.title = request.POST.get("title")
        if request.FILES.get("image"):
            blog.image = request.FILES.get("image")
        blog.category = request.POST.get("category")
        blog.body = request.POST.get("content")
        blog.save()
        messages.success(request, "Blog updated successfully")
        return redirect('/update/')
    return render(request, 'update_blog.html', {'blog': blog})



#delete blog module
@login_required(login_url='/login/')

def delete_blog(request, bid):
    blog = Blog.objects.get(id=bid)
    blog.delete()
    return redirect('/update/')