import django_filters
from .models import *

class BlogFilter(django_filters.FilterSet):


    class Meta:
        model = Blog
        fields = ['title']
