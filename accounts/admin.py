from django.contrib import admin
from .models import UserProfileInfo
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(UserProfileInfo)
