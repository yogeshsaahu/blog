from django.contrib import admin
from .models import Blog,BlogCategory,Contact,Subscribe
# Register your models here.
# admin.site.register(UserProfile)
admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(Contact)
admin.site.register(Subscribe)