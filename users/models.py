from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    profile_image=models.ImageField(upload_to='event_asset',blank=True,null=True,default='event_asset/default_image.jpg')
    phone=models.CharField(blank=True)

    def __str__(self):
        return self.username