from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:auction_id>/", views.item, name="item"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("comment/<int:auction_id>", views.comment, name="comment")

]