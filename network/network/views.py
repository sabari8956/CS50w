from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from .models import User, Post
import json


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# @login_required(login_url='login') # need to add a arg of username where we can pass username and get output
def view_profile(req, user):
    user = User.objects.get(username=user)
    followers_cnt = len(user.followers.all())
    following_cnt = len(user.following.all())
    follow_bool = False
    if req.user.is_authenticated:
        user_client = User.objects.get(pk=req.user.id)
        following = user_client.following.all()
        if user in following:
            follow_bool = True
    return render(req, "network/profile.html", {
        "username": user,
        "follwers_cnt":  followers_cnt,
        "following_cnt": following_cnt,
        "following": follow_bool
    })


def view_search(req):
    return render(req, "network/search.html")


@login_required
def create_post(req):
    if req.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(req.body)
    print(data)

    post_data = Post(user=req.user, content=data["content"])
    post_data.save()
    return JsonResponse({"Status":"Post Posted"}, status=200)


def search_user(req):
    if req.method != "POST":
        return JsonResponse({"error": "Expected Post method"}, status=400)
    
    data = json.loads(req.body)
    query = data.get("query", "")
    results_list = []
    if not query:
        return JsonResponse({"users": []}, status=200)
    
    results = User.objects.filter(username__icontains=query).values('id', 'username')
    results_list = [
        user
        for user in results.annotate(
            followers_count=models.Count('followers'),
            following_count=models.Count('following')
        )
    ]
    return JsonResponse({"users": results_list}, status=200)


@csrf_exempt
@login_required
def follow_unfollow(req):
    if req.method == "PUT":
        data = json.loads(req.body)
        data_bool = data.get("follow")
        data_user1 = User.objects.get(pk= req.user.id)
        data_user2 = User.objects.get(pk= int(data.get("user_id")))
        if data_bool == "True":
            data_user1.following.remove(data_user2)
        else:
            data_user1.following.add(data_user2)
        return JsonResponse({"status": "Done"}, status=200)
    return JsonResponse({"Error": "its should be post method"}, status=401)