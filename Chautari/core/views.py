from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post,LikePost, FollowersCount
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

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username = username).first()
    
    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username = username)
        new_like.save()
        post.likes+=1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.likes-=1
        post.save()
        return redirect('/')
    
@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = user_object)
    user_posts_length = len(user_posts)
    follower = request.user.username
    user = pk
    if FollowersCount.objects.filter(follower = follower, user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    follower_number = len(FollowersCount.objects.filter(user=pk)) #The followers of the profile thats being seen
    user_following = len(FollowersCount.objects.filter(follower=pk)) #The numbers of followers the profile is following
    
    context = {
        'user_object': user_object,
        'user_profile':user_profile,
        'posts': user_posts,
        'posts_length': user_posts_length,
        'button_text': button_text,
        'followers' : follower_number,
        'following' : user_following,
    }
    return render(request, 'profile.html',context )

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        follower_filter = FollowersCount.objects.filter(follower=follower, user = user).first()
        
        if follower_filter is not None:
            follower_filter.delete()
            return redirect('/profile/'+user)
        else:
            new_follow = FollowersCount.objects.create(follower=follower, user = user)
            new_follow.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')