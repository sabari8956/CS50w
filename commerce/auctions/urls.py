from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.create_listing, name="listing"),
    path("product/<int:p_id>", views.view_product, name="product"),
    path("category/", views.catagorys, name="category"),
    path("category/<str:filter>/", views.catagorys, name="category_filter"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
]
