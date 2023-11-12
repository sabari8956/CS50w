from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls.exceptions import NoReverseMatch
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .forms import *
from .models import *
from .util import *

from django.contrib import messages

def index(request):
    lsts_hb, wl_cnt = getListings(request)

    return render(request, "auctions/index.html", {
        "listings": lsts_hb,
        "wl_cnt": wl_cnt
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
            # if next in url return the value else render index

            try:
                nxt_url = request.POST.get('next', 'index') 
                nxt_url = nxt_url.split('/')
                if "product" in nxt_url[1]:
                    p_id = int(nxt_url[2])
                    return HttpResponseRedirect(reverse(nxt_url[1], kwargs={'p_id': p_id}))
            except:
                    return HttpResponseRedirect(reverse("index"))

            try :
                return HttpResponseRedirect(reverse(nxt_url[1:]))

            # if some error ocurrs it redirects to index
            except NoReverseMatch:
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
        
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create_listing(request):
    if request.method == 'POST':
        form = createListing(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            newListing = Listing(title=form_data["name"], 
                                description= form_data["description"], 
                                image_url= form_data["image_url"], 
                                base_price=form_data["base_bid"], 
                                user= User.objects.get(pk=request.user.id), 
                                catagory= Catagory.objects.get(pk=form_data["catagory"])
                                )
            newListing.save()
            return HttpResponseRedirect(reverse('product', kwargs={'p_id': newListing.id}))
    else:
        form = createListing()

    return render(request, "auctions/listing.html",{
        "catagorys" : Catagory.objects.all(),
        "form": form
    })

def view_product(request, p_id):
    if request.method == "POST" and 'form_type' in request.POST:
        form_type = request.POST['form_type']

        if form_type == 'wishlist-form':
            handleForm_wishlist(request, p_id)
            bid_form = createBids(listing_id=p_id)

        elif form_type == 'bidding-form':
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login') + '?next=' + request.path)
            form = createBids(request.POST, listing_id=p_id)

            if form.is_valid() and  form.cleaned_data['bid']:
                if not handleForm_bidding(request, p_id, form.cleaned_data['bid']):
                    messages.warning(request, "Some errore ocurred!")
                else:
                    messages.success(request, 'You have bided successfully.')
                return HttpResponseRedirect(reverse('product', kwargs={'p_id':p_id}))
            
            else:
                bid_form = createBids(request.POST, listing_id=p_id)
                messages.warning(request, "Bid for auction Price")
            
        elif form_type == "comment-form":
            form = createComment(request.POST)
            if form.is_valid():
                comment = form.cleaned_data["comment"]
                if not handleForm_comment(request, p_id, comment):
                    messages.warning(request, "Some error ocurred !")
                else:
                    messages.success(request, "comment added sucessfully !")
                
            bid_form = createBids(listing_id=p_id)
        elif form_type == "deleteListing-form":
            handleForm_deleteListing(p_id)
            messages.success(request,"Listing Deleted!")
            return HttpResponseRedirect(reverse('product', kwargs={'p_id':p_id}))
    else:
        bid_form = createBids(listing_id=p_id)

    product, highest_bid, comments, wishlist_value = getData_viewProduct(request,p_id)

    create_form = createComment()

    return render(request, "auctions/product.html",{
        "product": product,
        "wishlist_bool": wishlist_value,
        "bid_form": bid_form,
        "Current_Bid": highest_bid,
        "comment_form": create_form,
        "comments": comments
    })

def catagorys(request, filter=None):
    if request.POST:
        form_data = CatagoryFilter(request.POST)
        if form_data.is_valid():
            form_data = form_data.cleaned_data
            return HttpResponseRedirect(reverse('category_filter', kwargs={"filter": Catagory.objects.get(pk=form_data["catagory"]) }))
    
    if filter:
        catagory = [cat.__str__().lower() for cat in Catagory.objects.all()]
        if filter.lower() in catagory:
            filtered_listings = Listing.objects.filter(catagory=Catagory.objects.get(type=filter.capitalize()), listing_status=True)
            return render(request, "auctions/catagory.html",{
                "catagory_found": filter,
                "items":filtered_listings
            })

        else:
            return HttpResponseRedirect(reverse('category'))
     
    else:
        return render(request, "auctions/catagory.html",{
            "catagory_form": CatagoryFilter()
        })

@login_required(login_url='login')
def wishlist_view(request):

    lsts_hb = getWishlist(request)

    return render(request, "auctions/wishlist.html", {
        "listings": lsts_hb
    })

