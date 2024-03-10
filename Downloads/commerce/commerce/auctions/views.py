from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from datetime import datetime

from .models import CATEGORIES, User, Listing, Bids, Watchlist, Comment

sort_by_choices = {"datetime":"Date", "title":"Alphabetical", "price__bid":"Price"}

#Sorting form with choices and asc/desc checkbox
class sort_form(forms.Form):
    sort_by = forms.ChoiceField(required=False, label="",choices = sort_by_choices, widget=forms.Select(attrs={'onchange':'this.form.submit()', 'class': 'dropdown'}))
    asc = forms.BooleanField(label="test", required=False, widget=forms.CheckboxInput(attrs={'onchange':'this.form.submit()', 'class': 'checkbox'}))

#Startpage
def index(request):
    #If sorting form has been used
    if request.method == "POST":
        sort = request.POST["sort_by"]
        listings = Listing.objects.filter(isActive=True).order_by(sort)
        try:
            asc = request.POST["asc"]
            listings = listings.reverse()
        except:
            asc = "off"
        form = sort_form(request.POST)
        
        return render(request, "auctions/index.html", {
            'listings': listings,
            'bids': Bids.objects.all(),
            'form': form
        })
        
    else: 
        form = sort_form()
        return render(request, "auctions/index.html", {
            'listings': Listing.objects.filter(isActive=True).order_by('datetime'),
            'bids': Bids.objects.all(),
            'form': form
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
        
        listing = Listing(title=title, description=description, price=bid, seller=user, image = imageurl, category = category, datetime = now, )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/create_listing.html",{
        "CATEGORIES": CATEGORIES
    })
    
    
def listing_page_view(request, listing_id, isOnWatchlist = False):
    if request.method == "GET":
        listing = Listing.objects.get(id=listing_id) 
        
        bidMessage = request.GET.get('bidMessage', None)
        latestBidder = request.GET.get('bidder', None)
        
        user = request.user
        
        isOwner = False
        try: 
            comments = Comment.objects.filter(listing=listing)
            print(comments)
        except Comment.DoesNotExist:
            comments = None
            print("fail")
        
        
        if user == listing.seller:
            isOwner = True
        
        try: 
            Watchlist.objects.get(user=user, item_id=listing_id)
            isOnWatchlist = True
        except Watchlist.DoesNotExist:
            isOnWatchlist = False
        
        
        
        
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            'bids': Bids.objects.all(),
            'isOnWatchlist': isOnWatchlist,
            'bidMessage': bidMessage,
            'isOwner': isOwner,
            'latestBidder': latestBidder,
            'comments': comments,
            'user': user
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
        
        item_ids = [item.item_id for item in watchlist]

        listings = Listing.objects.filter(id__in=item_ids)

        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })
        
    except Watchlist.DoesNotExist:
        print("error")
        

def category_view(request):
    if request.method == "GET":
        return render(request, "auctions/categories.html", {
            'categories': CATEGORIES,
        })

def category_page_view(request, chosenCategory):
    if request.method == "GET":
        
        listings = Listing.objects.filter(category=chosenCategory)
        return render(request, "auctions/category_page.html", {
            'category': chosenCategory,
            'listings': listings,
        })

def bid(request, listing_id):
    if request.method == "POST":
        userBid = request.POST.get("bid")
        userBid = int(userBid)
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        
        if userBid > listing.price.bid:
            bid = Bids(bid=userBid, user=user)
            bid.save()
            
            listing.price = bid
            listing.save()
            
            bidder = user
            bidMessage = "Your bid has been placed"
        else:
            bidMessage = "Your bid must be higher than current bid"
    
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)) + f"?bidMessage={bidMessage}&bidder={bidder}")
    
    
def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        
        comment = request.POST.get("comment")
        
        listing = Listing.objects.get(pk=listing_id)
        
        saveComment = Comment(user=user, listing=listing, comment=comment)
        saveComment.save()
        
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
        
def closeAuction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        winner = listing.price.user
        print(winner)
        listing.isActive = False
        listing.winner = winner
        listing.save()
        
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

