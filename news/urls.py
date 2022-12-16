from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogSiteMap
from django.views.generic.base import TemplateView
from . import views



urlpatterns = [

    path('', views.index, name='index'),
    path('subscribe', views.subscribe, name='subscribe'),

    path('authors', views.author, name='author'),
    path('authors/<int:id>', views.author_details, name='author_details'),

    path('blog/<str:url>', views.Blogdetails, name='Blogdetails'),
    path('blog', views.blog, name='blog'),

    path('category', views.categories, name='categories'),
    path('category/<str:url>', views.category_details, name='category_details'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('add_blog', views.add_blog, name='add_blog'),
    path('about', views.about, name='about'),
    path('Privacy-Policy', views.Privacy, name='Privacy'),
    path('search/', views.search, name='search'),
    path('deleteblog/<int:id>',views.delete,name="delete"),
    path('add_blog/<int:id>', views.update, name="updateblog"),
    path('profile_update/<int:id>', views.profile_update, name="profile_update"),
    path('sitemap.xml', sitemap, {'sitemaps': {'blog': BlogSiteMap}},name='django.contrib.sitemaps.views.sitemap'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_tag'),
    path("robots.txt",TemplateView.as_view(
        template_name="main/robots.txt", content_type="text/plain")),
]