from .models import *
from .forms import *

# Utility Functions 

# Get Active Listings

def getListings(request):
    lsts_hb = []
    wl_cnt = 0
    for listing in Listing.objects.filter(listing_status=True):
        highest_bid = Bid.objects.filter(listing_id=listing.id).aggregate(Max('bid_amount'))['bid_amount__max']
        list_data = (listing, highest_bid)
        lsts_hb.append(list_data)

    if request.user.is_authenticated:
        watchlist = WatchList.objects.get(user=request.user)
        wl_cnt = len(watchlist.listings.all())

    return (lsts_hb, wl_cnt)
    
def handleForm_wishlist(request, p_id):
    watchlist = WatchList.objects.get(user=request.user)
    wl_listings = watchlist.listings.all()
    c_listing = Listing.objects.get(id=p_id)
    wl_ids = [item.id for item in wl_listings]
    if p_id in wl_ids:
        watchlist.listings.remove(c_listing)
    else:
        watchlist.listings.add(c_listing)

def handleForm_bidding(request, p_id, bid_amt):
    try:
        bid_data = Bid(
            user= request.user,
            listing_id= Listing.objects.get(id=p_id),
            bid_amount = bid_amt
        )
        bid_data.save()
        return True
    except:
        return False

def handleForm_comment(request, p_id, comment):
    try:
        comment_data = Comment(
            user= request.user,
            listing_id= Listing.objects.get(id=p_id),
            content= comment
        )
        comment_data.save()
        return True
    except:
        return False
    
def handleForm_deleteListing(p_id):
    highest_bidder = Bid.objects.filter(listing_id=p_id).annotate(max_bid=Max('bid_amount')).order_by('-max_bid').first()
    print(highest_bidder)
    if highest_bidder:
        listing = Listing.objects.filter(id=p_id).update(listing_status=False, winner=highest_bidder.user)
    else:
        listing = Listing.objects.filter(id=p_id).update(listing_status=False, winner=None)
        


def getData_viewProduct(request, p_id):
    product = Listing.objects.get(id=p_id)
    highest_bid = Bid.objects.filter(listing_id=p_id).aggregate(Max('bid_amount'))['bid_amount__max']
    comments = Comment.objects.filter(listing_id=p_id).order_by('-time_stamp')
    wl_val = False
    if request.user.is_authenticated:
        watchlist = WatchList.objects.get(user=request.user)
        wl_ids = [listing.id for listing in watchlist.listings.all()]
        if p_id in wl_ids:
            wl_val = True
    return (product, highest_bid, comments, wl_val)

def getWishlist(request):
    lsts_hb = []
    watchlist = WatchList.objects.get(user=request.user)
    wl_listings = watchlist.listings.all()
    for listing in wl_listings:
        highest_bid = Bid.objects.filter(listing_id=listing.id).aggregate(Max('bid_amount'))['bid_amount__max']
        list_data = (listing, highest_bid)
        lsts_hb.append(list_data)
    
    return lsts_hb
