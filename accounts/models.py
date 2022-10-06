from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    skills = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=400, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
    