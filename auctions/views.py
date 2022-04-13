from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from auctions.forms import formBid, formListing
from PIL import Image
import requests, json
from .models import User, Listing, Watchlist


def index(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
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
    

def createListing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == 'POST':
        form = (formListing(request.POST, request.FILES))
        if form.is_valid():
            
            f = Listing(
            title = form.cleaned_data["title"],
            description = form.cleaned_data["description"],
            startingBid = form.cleaned_data["startingBid"],
            imageLink = form.cleaned_data["imageLink"],
            category = form.cleaned_data["category"],
            user = User.objects.filter(id =request.user.id).first()
        
            )
            f.save()
            print(f)

            
            return HttpResponseRedirect(reverse("index"))
            
        else :
            # return HttpResponse("Sorry there's a problem with you form")
            return render (request, 'auctions/createListing.html', {
                "form" : form
            })
    
    else:
        return render (request, "auctions/createListing.html", {
            "form" : formListing()
        }) 

def displayListing(request, listingId):
    if request.user.is_authenticated:
        query = Watchlist.objects.filter(listing_id=listingId, user=request.user.id)
        if query.first():
             watchlistFlag = True
        else:
            watchlistFlag = False   
        
        return render (request, "auctions/displayListing.html", {
        "listing": Listing.objects.filter(id=listingId),
        "watchlistFlag": watchlistFlag,
        "form": formBid()
        })
    else:
        print ("Not logged")
        return HttpResponse("Apologies, log in")

def addItemToWatchlist(request):
    if request.method == 'POST':
        f = Watchlist(
        listing = Listing.objects.get(id = json.loads(request.body)),
        user = request.user
        )
        f.save()
    return JsonResponse({'Status':'Ok'})



def removeItemFromWatchlist(request):
    if request.method == 'POST':
       f = Watchlist.objects.get(
       listing = Listing.objects.get(id = json.loads(request.body)),
       user = request.user
       )
       f.delete() 
    return JsonResponse({'Status':'Ok'})

