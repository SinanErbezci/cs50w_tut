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
    description = models.CharField(max_length=256)
    image = models.URLField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ELSE)
    
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
