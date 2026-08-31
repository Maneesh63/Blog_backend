from uuid import uuid4
from django.db import models
from blog.models import Datetime

class User(Datetime):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

     
    def __str__(self):
        return self.email

class UserProfile(Datetime):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    extra_info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.user.email 
