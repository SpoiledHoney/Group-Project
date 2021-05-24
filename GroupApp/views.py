from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Post, Comment
from .forms import BlogForm
import bcrypt
# Create your views here.

def index(request):
    return render(request, 'index.html')

#Create User
def create_user(request):
    if request.method == "POST":
        #validation
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        #validation end
        

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['logged_user'] = new_user.id
        return redirect('/user/dashboard')
    return redirect("/")

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/user/dashboard')
        messages.error(request, "email or password are incorrect!")

    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if('logged_user' not in request.session):
        messages.error(request, "Login before you do that!")
        return redirect('/')
    user = User.objects.get(id=request.session['logged_user'])
    allPosts = Post.objects.all()
    context = { 
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'allPosts' : Post.objects.all,
    }
    return render(request, 'dashboard.html', context)

def blog_form(request):
    context = { 
        "Blog_Form":BlogForm
    }
    return render(request, 'post_form.html', context)

def CreatePost(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['logged_user'])
        PostedBlogForm = BlogForm(request.POST, request.FILES)
        if PostedBlogForm.is_valid():
            print(PostedBlogForm.data)
            NewPost = PostedBlogForm.save(commit=False)
            NewPost.user_post = User.objects.get(id=user.id)
            PostedBlogForm.save()
            return redirect('user/dashboard')
        else:
            context = {
                "Blog_Form": PostedBlogForm,
                'logged_user': User.objects.get(id=request.session['logged_user']),
            }
            return render(request, 'dashboard.html', context)
    return redirect('/dashboard')

def show_post(request, post_id):
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'post' : Post.objects.get(id=post_id)
    }
    return render(request, 'user_post.html', context)

def user_page(request, user_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    user = User.objects.get(id=user_id)

    context = {
        'one_user': user
    }
    return render(request, 'user_page.html', context)

def delete(request, post_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect(f'/user/dashboard')