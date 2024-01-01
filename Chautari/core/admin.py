from django.contrib import admin
from .models import Profile,Post,LikePost,FollowersCount

# Register your models here.To show in the admin panel
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)