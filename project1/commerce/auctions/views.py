from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import User, Auctions, Comments, Bids
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from decimal import Decimal


def index(request):
    items = Auctions.objects.filter(active=True)
    img_url = static('auctions/card-image.svg')
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
    user = User.objects.get(pk=request.user.id)

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

        if not category:
            category = "EL"   
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
                description=desc, category=category, image=url, initial_price=price, price=price, title=title, owner=user
                )
            new_item.save()
            return redirect("index")


    return render(request, "auctions/create_listing.html", {
        "category_dict": category_dict
    })

def listing(request,item_id):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        item = Auctions.objects.get(pk=item_id)
        if request.POST.get("watch",""):
            item = Auctions.objects.get(pk = item_id)
            if ( item.watchlist.filter(pk=request.user.id)):
                item.watchlist.remove(request.user.id)
                item.save()
                messages.success(request, "You've successfully removed from your watchlist")
            else:
                item.watchlist.set([request.user.id]) 
                item.save()
                messages.success(request, "You've successfully added to your watchlist")
        
        elif request.POST.get("comment",""):
            new_item = Comments.objects.create(
                message=request.POST["comment"], user=user, item=item
            )
            new_item.save()
            messages.success(request, "You've successfully commented")
        elif request.POST.get("bid",""):
            max_bid = Bids.objects.filter(item=item).order_by("-bid")
            if not max_bid:
                max_bid = float(item.price)
            else:
                max_bid = float(max_bid[0].bid)
            user_bid = float(request.POST["bid"])
            user_bid_dec = Decimal(user_bid).quantize(Decimal("1.00"))

            if user_bid < max_bid:
                messages.warning(request, "Please bid higher than max bid or initial price")
            else:
                new_bid = Bids.objects.create(
                    bid=user_bid_dec, user=user, item=item
                )
                new_bid.save()
                item.price = user_bid_dec
                item.save()
        elif request.POST.get("close",""):
            item.active = False
            buyer = Bids.objects.order_by("-bid").filter(item=item)[0].user
            item.buyer = buyer
            item.save()
            
        return redirect("listing", item_id=item_id)


    item = Auctions.objects.get(pk = item_id)
    comments = Comments.objects.all().select_related("user").filter(item=item).order_by("enter_time")
    bids = Bids.objects.all().filter(item=item).order_by("-bid")
    user_bid = watched = ""

    if not bids:
        bid_count = 0
        max_bid = ""
    else:
        if request.user.is_authenticated:
            user_bid = bids.filter(user=request.user)
            if not user_bid:
                user_bid = ""
            else:
                user_bid = user_bid[0].bid
        
        max_bid = bids[0].bid
        bid_count = bids.count()

    if item.watchlist.filter(pk=request.user.id):
        watched = True
    else:
        watched = False

    if item.owner.pk == request.user.id:
        owner = True
    else:
        owner = False

    img_url = static('auctions/card-image.svg')
    watch_url = static('auctions/add.svg')
    watched_url = static('auctions/add_fill.svg')
    if item:
        return render(request, "auctions/listing.html", {
            "item":item,
            "img_url":img_url,
            "watch_url":watch_url,
            "watched_url":watched_url,
            "watched":watched,
            "comments": comments,
            "user_bid": user_bid,
            "max_bid": max_bid,
            "bid_count": bid_count,
            "owner": owner
        })
    else:
        messages.warning(request, "Item is not active or not found")
        return redirect("index")
    
@login_required
def watchlist(request):
    items = Auctions.objects.filter(watchlist__id=request.user.id)
    print(items)
    return render(request, "auctions/watchlist.html", {
        "items":items
    })

def categories(request):
    category_dict = Auctions.CATEGORY_CHOICES
    items = ""
    category = request.GET.get('category', "")
    img_url = static('auctions/card-image.svg')
    if category:
        items = Auctions.objects.all().filter(category=category)
    return render(request, "auctions/categories.html", {
        "categories":category_dict,
        "items": items,
        "img_url": img_url
    })
