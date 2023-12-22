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

    if request.user.is_authenticated:
        following_posts = Post.objects.filter(user__in=request.user.following.all())
    else:
        following_posts = Post.objects.all()
    return render(request, "network/index.html", {
        "posts": following_posts
    })


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

def view_profile(req, user):
    user = User.objects.get(username=user)
    followers_cnt = len(user.followers.all())
    following_cnt = len(user.following.all())
    follow_bool = False
    my_Posts = Post.objects.filter(user= user.id)
    if req.user.is_authenticated:
        user_client = User.objects.get(pk=req.user.id)
        following = user_client.following.all()
        if user in following:
            follow_bool = True
    return render(req, "network/profile.html", {
        "username": user,
        "follwers_cnt":  followers_cnt,
        "following_cnt": following_cnt,
        "following": follow_bool,
        "posts": my_Posts
    })


def view_search(req):
    # print(Post.objects.all())
    return render(req, "network/search.html", {
        "posts": Post.objects.all()
    })


@login_required
def create_post(req):
    if req.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(req.body)

    post_data = Post(user=req.user, content=data["content"])
    post_data.save()
    return JsonResponse({"Status":"Post Posted"}, status=200)


def search_user(req):
    if req.method != "POST":
        return JsonResponse({"error": "Expected Post method"}, status=400)
    
    data = json.loads(req.body)
    query = data.get("query", "")
    if not query:
        return JsonResponse({"users": []}, status=200)
    
    results = User.objects.filter(username__icontains=query).values('id', 'username')
    Search_results = []
    for user in results:
        user_data = {}
        Search_user = User.objects.get(pk=user["id"])
        user_data["username"] = Search_user.username
        user_data["followers"] = len(Search_user.followers.all())
        user_data["following"] = len(Search_user.following.all())
        Search_results.append(user_data)
    return JsonResponse({"users": Search_results}, status=200)

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


@login_required

def handle_like(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        user = User.objects.get(pk=data["user_id"])
        post = Post.objects.get(pk=data["post"])

        like_status = data["like"] 
        
        if like_status:
            post.likes.add(user)
        else:
            post.likes.remove(user)

        post.save()

        return JsonResponse({"result": "Success"}, status=200)

    return JsonResponse({"error": "Invalid method"}, status=400)


def handle_comment(req):
    if req.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)
    
    data = json.loads(req.body)
    user = User.objects.get(pk=data["user_id"])
    post = Post.objects.get(pk=data["post_id"])

    comment_data = data["comment_data"]

    if comment_data.strip():
        Comment(post= post, user= user, body= comment_data).save()
        print(f"Comment Added by {user} -> {post}")
        return JsonResponse({"result": "Success"}, status=200)
    return JsonResponse({"error": "No Comment Data"}, status=200)


def view_post(req, post_id):
    post = Post.objects.get(pk= post_id)
    comments =[ {"name": x.user.username, "comment": x.body, "timestamp": x.timestamp} for x in post.comments.all()]
    postData = {
        "user": post.user.username,
        "content": post.content,
        "Likes": post.likes.count(),
        "timestamp": post.timestamp,
        "comments": comments
    }
    return JsonResponse({"postData": postData})
    

@csrf_exempt
def user_data(req):
    if req.method != "POST":
        return JsonResponse({"error": "wrong method use post"}, status=400)
    
    if req.user.is_authenticated:
        return JsonResponse({"username": req.user.username, "user_id": req.user.id}, status=200)
    
    return JsonResponse({"username": None, "user_id": None}, status=400)