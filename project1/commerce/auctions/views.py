from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import User, Auctions
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

def index(request):
    items = Auctions.objects.filter(active=True)
    img_url = static('auctions/card-image.svg')
    print(img_url)
    return render(request, "auctions/index.html", {
            "items":items,
            "img_url":img_url   
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login First")
        return redirect("login")

    category_dict = Auctions.CATEGORY_CHOICES
    error = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        desc = request.POST.get("description","")
        category = request.POST.get("category", "")
        url = request.POST.get("url","")
        price1 = request.POST.get("price-1",False)
        price2 = request.POST.get("price-2",0)
        validate = URLValidator()
        if url:
            try:
                validate(url)
            except ValidationError as e:
                error = e.message

        if not desc:
            error = "Please Enter description"
        elif not category:
            error = "Please Select category"
        elif not price1 or not price1.isdigit():
            error = "Please Enter Price"
        elif not title:
            error ="Please Enter Title"
        
        if error:
            return render(request, "auctions/create_listing.html", {
            "category_dict": category_dict,
            "error": error
            })
        else:
            messages.success(request, "You've successfully created a listing")
            price = int(price1) + (int(price2)/100.0)
            new_item = Auctions.objects.create(
                description=desc, category=category, image=url, price=price, title=title
                )
            new_item.save()
            return redirect("index")


    return render(request, "auctions/create_listing.html", {
        "category_dict": category_dict
    })

def listing(request,item_id):
    if request.method == "POST":
        item = Auctions.objects.get(pk = item_id)
        if ( item.watchlist.filter(pk=request.user.id)):
            item.watchlist.remove(request.user.id)
            item.save()
        else:
            item.watchlist.set([request.user.id]) 
            item.save()

    item = Auctions.objects.get(pk = item_id)
    if item.watchlist.filter(pk=request.user.id):
        watched = True
    else:
        watched = False
    img_url = static('auctions/card-image.svg')
    watch_url = static('auctions/add.svg')
    watched_url = static('auctions/add_fill.svg')
    
    if item:
        return render(request, "auctions/listing.html", {
            "item":item,
            "img_url":img_url,
            "watch_url":watch_url,
            "watched_url":watched_url,
            "watched":watched
        })
    else:
        messages.warning(request, "Item is not active or not found")
        return redirect("index")
    
