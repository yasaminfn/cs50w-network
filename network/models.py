from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like =models.IntegerField(default=0)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.account} posted {self.content}."
    
class Account(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="accounts")
    #post = models.ForeignKey("Post", related_name="account") -> it has already been related in the Post class
    following = models.ManyToManyField("Account", symmetrical=False, blank=True, related_name="follower") #symmetrical=False -> not every following follows you
    
    
    def __str__(self):
        return self.owner.username

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} liked {self.post}."

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented {self.content}."
