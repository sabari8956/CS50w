from django.contrib.auth.models import AbstractUser
from django.db import models




class Catagory(models.Model):
    type = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type}"

class User(AbstractUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        WatchList.objects.get_or_create(user=self)


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    image_url = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owns') # when we want to get all the listings that the user owns we use user.owns.all()
    time_stamp = models.DateTimeField(auto_now_add=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    listing_status = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="wins")

    def __str__(self) -> str:
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} [{self.listing_id.title}] -> ${self.bid_amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.content} -> {self.listing_id}"
    

class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True)

    def __str__(self) -> str:
        return f"{self.user}"