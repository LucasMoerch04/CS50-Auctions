from django.contrib import admin
from .models import User, Listing, Bids, Watchlist, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(Comment)