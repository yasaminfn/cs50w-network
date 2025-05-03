
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("post/<int:post_id>", views.get_post, name="post-detail"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow, name = "follow"),
    path("unfollow/<str:username>", views.unfollow, name = "unfollow"),
    path("followings", views.following, name = "following"),
    path("edit/<int:post_id>", views.edit, name = "edit"),

]
