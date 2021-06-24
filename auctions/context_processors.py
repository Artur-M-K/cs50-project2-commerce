from .models import Watchlist, Auction_listings


def watchlist_all(request):
    user = request.user.is_authenticated
    if user:
        watchlist = Watchlist.objects.filter(author=request.user)
        return {'watchlist_all': watchlist}
    else:
        auctions = Auction_listings.objects.filter(active=True)
        return {'auctions': auctions}
