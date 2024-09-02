from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User,Post, Follow
import json


def index(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        content = request.POST["content"]
        post = Post.objects.create(content=content, owner=user)
        post.save()            
        return HttpResponseRedirect(reverse("index"))

    posts = Post.objects.all().order_by("-time")
    paginator = Paginator(posts,10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "network/index.html", {'page_obj': page_obj})


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.all().filter(owner=user).order_by("-time")
    out = {"posts" : posts, "username":username}

    if (not request.user.is_authenticated) or (username == request.user.username):
        out["button"] = False
    else:
        follower  = User.objects.get(pk = request.user.id)
        try: 
            Follow.objects.get(follower = follower, following=user)
            print("yes")
            follow = True
        except:
            print("no")
            follow = False
        out["follow"] = follow
        out["button"] = True

    return render(request, "network/profile.html", out)



# API
@login_required
@csrf_exempt
def follow(request, username):
    if request.method == "POST":
        follower = User.objects.get(pk=request.user.id)
        following = User.objects.get(username=username)
        data = json.loads(request.body)
        if data["text"] == "follow":
            follow = Follow.objects.create(follower = follower, following= following)
            follow.save()
        elif data["text"] == "unfollow":
            follow = Follow.objects.get(follower = follower, following= following)
            follow.delete()
    return redirect("index")

