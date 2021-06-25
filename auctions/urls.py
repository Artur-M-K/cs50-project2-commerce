from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:auction_id>/", views.item, name="item"),
    path("auctionend/<int:auction_id>", views.auctionend, name="auctionend"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("watchlist_add/<int:auction_id>",
         views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:auction_id>",
         views.watchlist_remove, name="watchlist_remove"),
    path("watchlist", views.watchlist, name="watchlist")

]
