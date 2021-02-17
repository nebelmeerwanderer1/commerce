from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    photo_link = models.URLField()
    seller = models.ForeignKey(User, related_name="seller", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name="category", on_delete=models.SET_NULL, null=True)
    active = models.BooleanField()
    creation_time = models.TimeField(auto_now_add=True)
    last_edit = models.TimeField(auto_now=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.id}: {self.title}"

class Comment(models.Model):
    comment = models.CharField(max_length=512)
    listing = models.ForeignKey(Listing, related_name="object", on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.SET_NULL, null=True)
    creation_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.creator}"

class Bid(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, related_name="listing", on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, related_name="buyer", on_delete=models.SET_NULL, null=True)
    creation_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.bid} for {self.listing}"





