from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

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
        
        return redirect("index") 

def profile(request, username):
    print(username)
    owner = User.objects.get(username=username)
    account = Account.objects.get(owner=owner)
    print(account.following.all())
    return render(request, "network/profile.html",{
        "user": owner,
        "account": account,
        "post" : account.posts.all()
    })
def follow(request):
    pass


def unfollow(request):
    pass

def like(request):
    pass

def edit(request):
    pass
