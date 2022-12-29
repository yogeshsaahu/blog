from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django.urls import reverse
from django_resized import ResizedImageField
from autoslug import AutoSlugField


# this modal for blog categorys form
class BlogCategory(models.Model):
      category = models.CharField(max_length=100)
      category_details = models.CharField(max_length=250, blank=True)
      slug = AutoSlugField(populate_from='category')
      created = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return self.category





# this modal for blog form
class Blog(models.Model):
      category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
      snipit = models.CharField(max_length=200)
      title = models.CharField(max_length=250)
      img_opt = models.BooleanField()
      img = ResizedImageField(size=[1020, 660], upload_to='pics',blank=True,null=True)
      img_alt = models.CharField(max_length=250, blank=True,null=True)
      description = models.TextField()
      reading_time = models.IntegerField(default=2)
      blog_url = AutoSlugField(populate_from='title')
      author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
      title_meta = models.CharField(max_length=250)
      description_meta = models.CharField(max_length=700)
      keywords_meta = models.CharField(max_length=250)
      is_active = models.BooleanField(default=False)
      created = models.DateTimeField(auto_now_add=True)
      tags = TaggableManager()

      def get_absolute_url(self):

            return reverse("Blogdetails", kwargs={"blog_url": str(self.blog_url)})

      def __str__(self):
            return self.title



# this modal for contact form
class Contact(models.Model):
      name = models.CharField(max_length=50)
      email = models.EmailField(max_length=100)
      subject = models.CharField(max_length=100)
      message = models.TextField()
      created = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return self.name




class Subscribe(models.Model):
      name = models.CharField(max_length=50)
      email = models.EmailField(max_length=100, unique=True)

      def __str__(self):
            return self.name


class Post_of_the_month(models.Model):
      select = models.ForeignKey(Blog, on_delete=models.CASCADE)
      updated = models.DateTimeField(auto_now=True)

      def __str__(self):
            return self.select







