from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Blog,BlogCategory,Contact,Subscribe,Post_of_the_month
# Register your models here.
# admin.site.register(UserProfile)
# admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(Contact)
admin.site.register(Subscribe)
admin.site.register(Post_of_the_month)


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)

admin.site.register(Blog, PostAdmin)