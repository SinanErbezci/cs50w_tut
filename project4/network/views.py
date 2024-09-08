from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User,Post, Follow, Like
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
    paginator = Paginator(posts,10) 
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    following = len(user.follower.all())
    follower = len(user.following.all())
    out = {"page_obj" : page_obj, 
    "username":username,
    "following":following,
    "follower":follower
    }   

    if (not request.user.is_authenticated) or (username == request.user.username):
        out["button"] = False
    else:
        follower  = User.objects.get(pk = request.user.id)
        try: 
            Follow.objects.get(follower = follower, following=user)
            follow = True
        except:
            follow = False
        out["follow"] = follow
        out["button"] = True

    return render(request, "network/profile.html", out)

@login_required
def following(request):
    user = User.objects.get(pk=request.user.id)
    following = user.follower.all()

    if len(following) == 0:
        nofollow = True
        page_obj = None
    else:
        nofollow = False
        follow = [x.following.id for x in following]
        out = Post.objects.all().filter(owner__id__in = follow)    

        paginator = Paginator(out,10) 
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        # {"page_obj":out, "nofollow":nofollow}

    return render(request, "network/following.html", {"page_obj":page_obj, "nofollow":nofollow})

# APIs
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

@login_required
@csrf_exempt
def like(request, post_id):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        post = Post.objects.get(pk=post_id)
        try:
            like = Like.objects.get(liker=user, liked=post)
            like.delete()
            post.like -= 1
            post.save()
            return JsonResponse({"out":"like removed"})
        except:
            new_like = Like.objects.create(liker=user, liked  = post)
            new_like.save()
            post.like += 1
            post.save()
            return JsonResponse({"out":"liked"})


    return redirect("index")

@login_required
@csrf_exempt
def edit(request, post_id):
    if request.method == "PATCH":
        post = Post.objects.get(pk=post_id)
        if (request.user.id == post.owner.id):
            data = json.loads(request.body)
            if data.get("content") is not None:
                content = data["content"]
                if content:
                    post.content = content
                    post.save()
                    return JsonResponse({"success":"yes"})
                else:
                    return JsonResponse({"success":"no"})

        else:
            return HttpResponseForbidden("<h1>You've been a bad boy</h1>")

    return redirect("index")