from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    startingBid = models.DecimalField (max_digits=5, decimal_places =2)
    imageLink = models.ImageField(max_length=100, null=True, blank=True, upload_to='images/', default='media/images/no.jpeg')
    category = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    # TO DO perhaps enum for categories?

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['user', 'listing']

    def __str__(self):
       return "%s %s"  % (self.user, self.listing)

class bids (models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.value, self.user, self.listing)


 


