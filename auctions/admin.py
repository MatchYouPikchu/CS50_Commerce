from django.contrib import admin
from .models import Listing, Watchlist, Bids

admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Bids)

# Register your models here.
