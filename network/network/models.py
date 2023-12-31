from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        liked_users = ', '.join([user.username for user in self.likes.all()])
        return f"Post by {self.user.username} -> {self.content} <> lIke: {liked_users}"

    
    class Meta:
        ordering = ['-timestamp']

class Comment(models.Model): 
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   body = models.TextField()
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self): 
       return 'Comment by {} on {}'.format(self.user.username, self.post)
