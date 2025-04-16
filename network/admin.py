from django.contrib import admin  

from .models import Post, Account, Like, Comment  

# Register your models here.  
admin.site.register(Post)  
admin.site.register(Account)  
admin.site.register(Like)  
admin.site.register(Comment)  