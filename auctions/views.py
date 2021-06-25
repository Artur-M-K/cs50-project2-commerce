from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm
from django.utils import timezone
from django import forms

from .models import User, Auction_listings, Bid, Category, Comment, Watchlist


class CreateListing(forms.ModelForm):
    class Meta:
        model = Auction_listings
        fields = ('image_url', 'title', 'description', 'price', 'category')
        exclude = ('author', 'created')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class PlaceBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['place_bid']
        exclude = ['author']


class AddComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


def index(request):

    auctions = Auction_listings.objects.filter(active=True)
    category = Category.objects.all()

    # return render(request, "auctions/index.html", {
    #     "auctions": auctions,
    #     "categories": category,

    # })
    if request.method == "POST":
        choices = request.POST.get('choice')
        # print(choices)
        if choices == '1':
            # print(choices)
            auctions = Auction_listings.objects.all()
            return render(request, "auctions/index.html", {
                "auctions": auctions,
                "categories": category,
            })

        if choices != '1':
            print(choices)
            auctions = Auction_listings.objects.filter(category=choices)
            return render(request, "auctions/index.html", {
                "auctions": auctions,
                "categories": category,
            })
    # else:
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "categories": category,

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
def create(request):
    if request.method == 'POST':
        form = CreateListing(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListing
    return render(request, "auctions/create.html", {
        'form': form
    })
    # return render(request, "auctions/index.html", {
    #     "auctions": Auction_listings.objects.all()
    # })


def item(request, auction_id):
    auction = Auction_listings.objects.get(id=auction_id)
    bids = Bid.objects.filter(auction=auction)
    last_bid = Bid.objects.all().reverse().last()
    comments = Comment.objects.filter(auction=auction)
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
            author=request.user, auction=auction).exists()

    if not request.user.is_authenticated:
        watchlist = None
        return HttpResponseRedirect(reverse("login"))

    actual_bid = auction.price

    if bids is not None:
        for bid in bids:
            if bid.place_bid > actual_bid:
                actual_bid = bid.place_bid

    return render(request, "auctions/item.html", {
        'auction': auction,
        'auction_id': auction_id,
        'bids': bids,
        'price': actual_bid,
        'min_bid': actual_bid+1,
        'last': last_bid,
        'comments': comments,
        'watchlist': watchlist

    })


@login_required
def bid(request, auction_id):

    auction = Auction_listings.objects.get(id=auction_id)
    if request.method == 'POST':
        form = PlaceBid(request.POST or None)
        if form.is_valid:
            user = request.user
            value = request.POST['bid']
            bid = Bid.objects.create(
                date=timezone.now(), author=user, place_bid=value, auction=auction)
            bid.save()
            auction.price = value
            auction.save(update_fields=['price'])
    return HttpResponseRedirect(reverse("item", kwargs={'auction_id': auction_id}))


@login_required
def comment(request, auction_id):
    auction = Auction_listings.objects.get(id=auction_id)
    if request.method == 'POST':
        form = AddComment(request.POST or None)
        if form.is_valid:
            user = request.user
            comment = request.POST.get('comment', None)
            newComment = Comment.objects.create(
                date=timezone.now(), author=user, comment=comment, auction=auction)
            newComment.save()

    return HttpResponseRedirect(reverse("item", kwargs={'auction_id': auction_id}))


@login_required
def watchlist_add(request, auction_id):
    auction = Auction_listings.objects.get(id=auction_id)

    if Watchlist.objects.filter(author=request.user, auction=auction).exists() == False:
        watchlist = Watchlist(author=request.user, auction=auction)
        watchlist.save()
    return redirect('item', auction_id=auction_id)


@login_required
def watchlist_remove(request, auction_id):
    auction = Auction_listings.objects.get(id=auction_id)
    if Watchlist.objects.filter(author=request.user, auction=auction).exists():
        Watchlist.objects.filter(author=request.user, auction=auction).delete()
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def watchlist(request):
    auctions = Watchlist.objects.filter(author=request.user)
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions,

    })


@login_required
def auctionend(request, auction_id):
    auction = Auction_listings.objects.get(id=auction_id)
    if auction.author == request.user:
        auction.active = False
        auction.save()
        messages.success(
            request, f'Auction for {auction.title} successfully closed!')
    return HttpResponseRedirect(reverse("item", kwargs={'auction_id': auction_id}))
