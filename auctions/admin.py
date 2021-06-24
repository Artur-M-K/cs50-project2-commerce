from django.contrib import admin

# Register your models here.
from .models import User, Auction_listings, Bid, Category, Comment, Watchlist

admin.site.register(User)
admin.site.register(Auction_listings)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Watchlist)
