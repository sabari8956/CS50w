
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.view_profile, name="profile"),
    path("search/", views.view_search, name="search"),


    # APIs 
    path('post', views.create_post, name="create_post"),
    path('finduser', views.search_user, name="find_user"),
    path('follow', views.follow_unfollow, name="followapi"),
    path("addlike", views.handle_like, name="likes"),
    path("addcomment", views.handle_comment, name="comment"),
    path("post/<int:post_id>", views.view_post, name="postapi"),
    path("auth", views.user_data, name="users_data"),
]
