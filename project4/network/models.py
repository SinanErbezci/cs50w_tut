from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=256)
    like = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User,related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User,related_name="following", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name="unique_followers")
        ]