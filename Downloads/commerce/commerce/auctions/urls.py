from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_page_view, name="listing_page"),
    path("edit_watchlist/<int:listing_id>", views.edit_watchlist_view, name="edit_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("closeAuction/<int:listing_id>", views.closeAuction, name="closeAuction"),
    path("category", views.category_view, name="category"),
    path("category_page/<str:chosenCategory>", views.category_page_view, name="category_page")
]
