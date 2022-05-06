from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from auctions.forms import formBid, formListing, formComment
from PIL import Image
import requests, json
from .models import User, Listing, Watchlist, Bids, listingComments


def index(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(active=True)
    })

def userWatchlist(request):
    listingList= Listing.objects.filter(included__pk__in = Watchlist.objects.all().values_list('id',flat=True), user=request.user)


    return render(request, "auctions/index.html",{
        "listings" : listingList
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
            return HttpResponseRedirect(reverse("index"))
            
        else :
            return render (request, 'auctions/createListing.html', {
                "form" : form
            })
    
    else:
        return render (request, "auctions/createListing.html", {
            "form" : formListing()
        }) 

def displayListing(request, listingId):
  
    queryWatchlist = Watchlist.objects.filter(listing_id=listingId, user=request.user.id).first()
    currentListing = Listing.objects.get(id=listingId)
    
 
    if currentListing.active == False:
        try:
            winnerFlag = Bids.objects.filter(listing_id=listingId).latest('value')
        except:
            winnerFlag = "None"
        return render (request, "auctions/closedListing.html",{
            "winnerFlag" : winnerFlag
        })
    else:

        if queryWatchlist:
            watchlistFlag = True
        else:
            watchlistFlag = False
    
        
        return render (request, "auctions/displayListing.html", {
        "listing": Listing.objects.filter(id=listingId),
        "watchlistFlag": watchlistFlag,
        'creatorFlag' : currentListing.isAuthor(request.user),
        "formBid": formBid(),
        "formComment" : formComment(),
        "comments" : listingComments.objects.filter(listing_id=listingId)
        })


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

def submitBid(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bidValue = data[1]
        listingId = data[0]

        if float(bidValue) <= compareBids(listingId):
            return JsonResponse({"Status": "Sorry, bid higher"})
        else:
            f = Bids(
            listing = Listing.objects.get(id = listingId),
            value = bidValue,
            user = request.user
            )
            f.save()
            return JsonResponse({'Status':'Ok'})
    
def compareBids(listing):
    startingBid = Listing.objects.filter(pk=listing).first()
    try:
        highestBid = Bids.objects.filter(listing_id=listing).latest('value')
    except:
        return 0
    return max(startingBid.startingBid, highestBid.value)
   

def closeListing(request):
    if request.method =="POST":
        Listing.objects.filter(id = json.loads(request.body)).update(active=False)
        return JsonResponse({'Status':'Ok'})

def submitComment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        commentValue = data[1]
        listingId = data[0]
        f = listingComments(
           listing = Listing.objects.get(id = listingId),
            comment = commentValue,
            user = request.user
            )
        f.save()
        return JsonResponse ({"Status" : "ok"})

def categories(request):
    if request.method == "POST":
        return render(request,"auctions/index.html", {
            "listings": Listing.objects.filter(category=request.POST['category'])
        } )
    else:
        return render(request, "auctions/categories.html", {
        "categories": Listing.objects.filter(active = True).values_list('category', flat=True)
        })
   



