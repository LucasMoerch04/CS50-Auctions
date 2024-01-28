from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .models import CATEGORIES, User, Listing, Bids, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all(),
        'bids': Bids.objects.all()
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

@login_required    
def create_listing_view(request):
    if request.method =="POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["price"]
        user = request.user
        imageurl = request.POST["imageurl"]
        category = request.POST["category"]
        now = datetime.now()
        
        bid = Bids(bid=int(starting_bid), user=user)
        bid.save()
        
        listing = Listing(title=title, description=description, price=bid, seller=user, image = imageurl, category=category, datetime = now)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/create_listing.html",{
        "CATEGORIES": CATEGORIES
    })
    
def listing_page_view(request, listing_id, isOnWatchlist = False):
    if request.method == "GET":
        listing = Listing.objects.get(id=listing_id) 
        
        user = request.user
        try: 
            Watchlist.objects.get(user=user, item_id=listing_id)
            isOnWatchlist = True
        except Watchlist.DoesNotExist:
            isOnWatchlist = False
        
        
        
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            'bids': Bids.objects.all(),
            'isOnWatchlist': isOnWatchlist
            })
        
def edit_watchlist_view(request, listing_id):
    if request.method == "POST":
        user = request.user
        try: 
            watchlist = Watchlist.objects.get(user=user, item_id=listing_id)
            watchlist.delete()
        except Watchlist.DoesNotExist:
            addToWatchlist = Watchlist.objects.create(item_id = listing_id, checked=False)
            addToWatchlist.user.add(user)

            
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

def watchlist_view(request):
    currentUser = request.user
    
    try: 
        watchlist = currentUser.watchlistUser.all()
        
        print(watchlist)
          # Get the IDs of the items in the watchlist
        item_ids = [item.item_id for item in watchlist]

        # Filter Listing objects based on the IDs in the watchlist
        listings = Listing.objects.filter(id__in=item_ids)

        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })
        
    except Watchlist.DoesNotExist:
        print("error")