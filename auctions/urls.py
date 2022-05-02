from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listing/<int:listingId>/", views.displayListing, name="displayListing"),
    path("addItemToWatchlist", views.addItemToWatchlist, name = "addItemToWatchlist"),
    path("removeItemFromWatchlist", views.removeItemFromWatchlist, name = "removeItemFromWatchlist"),
    path("submitBid", views.submitBid, name="submitBid"),
    path("closeListing", views.closeListing, name ='closeListing'),
    path("submitComment", views.submitComment, name="submitComment"),
    path("watchlist", views.userWatchlist, name="userWatchlist"),
    path("categories", views.categories, name="categories")

]