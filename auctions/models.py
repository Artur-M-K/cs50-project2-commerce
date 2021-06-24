from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    pass


class Category(models.Model):
    choices = [('all', 'all'), ('video games', 'video games'), ('cars', 'cars'), ('home equipment', 'home equipment'),
               ('clothes', 'clothes'), ('electronic devices', 'electronic devices'), ('others', 'others')]

    name = models.CharField(max_length=128, choices=choices)

    def __str__(self):
        return self.name


class Auction_listings(models.Model):
    image_url = models.CharField(max_length=1000)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=1000)
    created = models.DateTimeField(default=timezone.now, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    place_bid = models.DecimalField(decimal_places=2, max_digits=1000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    auction = models.ForeignKey(
        Auction_listings, on_delete=models.CASCADE)

    def __str__(self):
        # return f"{self.id} : {self.author.username} bid {self.place_bid} on {self.auction.title} at {self.date}"
        return self.author.username


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=256)
    auction = models.ForeignKey(
        Auction_listings, on_delete=models.CASCADE)

    def __str__(self):

        return self.author.username


class Watchlist(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auction = models.ForeignKey(
        Auction_listings, on_delete=models.CASCADE)
    added = models.BooleanField(default=False)

    def __str__(self):

        return self.author.username
