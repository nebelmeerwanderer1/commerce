from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {"listings": Listing.objects.exclude(active=False).all()})


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

def viewlisting(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    bids = listing.listing.all()
    try:
        currentbid = max(bids)
    except ValueError: 
        currentbid = None
    return render(request, "auctions/viewlisting.html", {
        "listing": listing,
        "currentbid": currentbid    
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.exclude(active=False).all(),
        "user": User.objects.get(username=request.user)
        })

def categories(request):
    return render(request, "auctions/categories.html", {"categories": Category.objects.all()})

def addtowatchlist(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        
        listing = Listing.objects.get(pk = int(listing_id))
        
        listing.watchlist.add(user)
        return HttpResponseRedirect(reverse("viewlisting", args=(listing.id,)))
