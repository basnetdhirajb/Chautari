from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

#Model of the currently logged in user
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images',default='default_profile.png')
    location = models.CharField(max_length= 100, blank = True)
    
    def __str__(self) -> str:
        return self.user.get_username()
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    createdOn = models.DateTimeField(default = datetime.now)
    likes = models.IntegerField(default = 0)
    
    
    def __str__(self) -> str:
        return self.caption
    