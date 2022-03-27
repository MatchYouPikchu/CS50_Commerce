from email.policy import default
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
 


