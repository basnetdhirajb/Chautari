from django.contrib import admin
from .models import Profile,Post

# Register your models here.To show in the admin panel
admin.site.register(Profile)
admin.site.register(Post)