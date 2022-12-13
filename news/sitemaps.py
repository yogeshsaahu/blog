from django.contrib.sitemaps import Sitemap
from .models import Blog

class BlogSiteMap(Sitemap):

    def items(self):
            return Blog.objects.all()

    def lastmod(self, obj):
            return obj.created

    def location(self, obj):
        return '/blog/%s' % (obj.blog_url)