from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-page/", views.new_page, name="new-pg"),
    path("search/", views.search, name="search"),
    path("<str:entry>", views.url_direct, name="redir"),
    path("search/<str:entry>", views.url_direct, name="redir"),
    path("random-pg/", views.random_page, name="random-pg"),
    path("edit/<str:entry>", views.edit_pg, name="edit-pg"),
]
