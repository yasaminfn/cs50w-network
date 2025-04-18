from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post, Account, Like, Comment


def index(request):
    post = Post.objects.all()
    return render(request, "network/index.html",{
        "post" : post,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Account.objects.create(owner=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request):
    print("form recieved")
    if request.method == "POST":
        
        currentuser=request.user
        account = currentuser.accounts.first()
        print(account)
        content = request.POST["content"]
        print(content)

        if account and content:
            newpost = Post(
                account = account,
                content = content,
                like = 0,

            ) 
            newpost.save()
        
        return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    owner = User.objects.get(username=username) #user
    account = Account.objects.get(owner=owner) #account
    currentuseraccount = request.user.accounts.first()
    print(account, currentuseraccount)
    if account != currentuseraccount:
        owns = False
        if account in currentuseraccount.following.all():
            follows= True
        else:
            follows = False
    else:
        owns = True
        follows = False

    return render(request, "network/profile.html",{
        "user": owner,
        "account": account,
        "post" : account.posts.all(),
        "follows" : follows,
        "owns" : owns,
    })


def follow(request, username):
    user = request.user #current user
    users_account=user.accounts.first() #current user's account
    profile = User.objects.get(username=username) #the user we wanna follow
    owner = Account.objects.get(owner=profile) #the account we wanna follow
    
    print(f"user: {user} profile: {profile} owner:{owner} user's account :{users_account}")
    if users_account != owner:
        if owner not in users_account.following.all():
            users_account.following.add(owner)
            print(f"added {owner} to the followings")
        else:
            print("already followed")
    else:
        print("You can't follow yourself!")
    
    return render(request, "network/profile.html",{
        "user": profile,
        "account": owner,
        "post" : owner.posts.all(),
        "follows" : True,
        "owns" : False,
    })



def unfollow(request, username):
    user = request.user #current user
    users_account=user.accounts.first() #current user's account
    profile = User.objects.get(username=username) #the user we wanna unfollow
    owner = Account.objects.get(owner=profile) #the account we wanna unfollow
    
    print(f"user: {user} profile: {profile} owner:{owner} user's account :{users_account}")
    if users_account != owner:
        if owner in users_account.following.all():
            users_account.following.remove(owner)
            print(f"removed {owner} from the followings")
        else:
            print("not following!")
    else:
        print("You can't unfollow yourself!")

    return render(request, "network/profile.html",{
        "user": profile,
        "account": owner,
        "post" : owner.posts.all(),
        "follows" : False,
        "owns" : False,
    })

@login_required(login_url="login")
def following(request):
    user=request.user #currentuser
    account=user.accounts.first() #currents user's account
    followings=account.following.all() #current user's followings
    posts=Post.objects.filter(account__in=followings)  #posts of user's followings
    
    if not posts.exists():
        return render(request, "network/index.html",{
        "post" : posts,
        "message" : "You’re not following anyone yet! Start exploring and follow users to see their posts"
    })

    return render(request, "network/index.html",{
        "post" : posts,
    }) 


def like(request):
    pass

def edit(request):
    pass
