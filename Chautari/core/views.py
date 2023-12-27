from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object =  User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    posts = Post.objects.all()
    return render(request,'index.html',{'user_profile':user_profile,'posts':posts})

def signin(request):
    
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        #check if the user exists with the given username and password
        user = auth.authenticate(username=username, password=password)
        
        #If user found
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Incorrect credentials')
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        #pull the data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('signup')
            else:
                #User needs to be created
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                
                
                #creating a new user profile
                userModel = User.objects.get(username=username)
                newProfile = Profile.objects.create(user = userModel, id_user = userModel.id)
                newProfile.save()
                
                return redirect('settings')
                
        else:
            messages.info(request, 'Passwords did not match')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        #If no image is sent in the request
        if request.FILES.get('profileimage') == None:
            image = user_profile.profileimg
        else:
            #getting the image file through the request
            image = request.FILES.get('profileimage')
        bio = request.POST['bio']
        location = request.POST['location']
        user_profile.profileimg = image
        user_profile.bio=bio
        user_profile.location=location
        user_profile.save()
        return redirect('/settings')
    
    return render(request, 'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image = image, caption = caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
