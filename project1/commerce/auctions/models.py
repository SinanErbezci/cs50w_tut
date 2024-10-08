from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auctions(models.Model):
    ELECTRONICS = "ER"
    FASHION = "FS"
    HOME = "HM"
    ELSE = "EL"
    CATEGORY_CHOICES = {
        ELECTRONICS: "Electronics",
        FASHION: "Fashion",
        HOME: "Home",
        ELSE: "Everything Else",
    }
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256,default='', blank=True)
    image = models.URLField(default='',blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    initial_price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ELSE)
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, default="", blank=True, on_delete=models.SET_NULL, null=True)
    
class Comments(models.Model):
    message = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Auctions,on_delete=models.CASCADE, related_name="item")
    enter_time = models.DateTimeField(auto_now_add=True)

class Bids(models.Model):
    bid = models.DecimalField(max_digits=12, decimal_places=2)
    item = models.ForeignKey(Auctions,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    enter_time = models.DateField(auto_now_add=True)
