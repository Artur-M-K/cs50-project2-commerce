from .models import Watchlist


def watchlist_all(request):
    watchlist = Watchlist.objects.filter(author=request.user)
    return {'watchlist_all': watchlist}
