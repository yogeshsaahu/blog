from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
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
    path('search/', views.search, name='search'),
    path('deleteblog/<int:id>',views.delete,name="delete"),
    path('add_blog/<int:id>', views.update, name="updateblog"),
    path('profile_update/<int:id>', views.profile_update, name="profile_update")
]