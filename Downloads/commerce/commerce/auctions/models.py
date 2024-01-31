from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = {
    "Electronics": "Electronics",
    "Clothes": "Clothes",
    "Accessories": "Accessories",
    "Health and Beauty": "Health and Beauty",
    "Other" : "Other"
}

class User(AbstractUser):
    pass

class Bids(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='userBid')
    
    
class Watchlist(models.Model):
    item_id = models.IntegerField(blank=True, null=True)    
    user = models.ManyToManyField(User, blank=True, related_name="watchlistUser")
    checked = models.BooleanField(blank=True, null=True)

    
class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=600)
    price = models.ForeignKey(Bids, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=20, choices = CATEGORIES, default="Category", null=True, blank=True)
    image = models.URLField(max_length=200, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    