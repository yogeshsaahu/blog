from django import forms
from .models import Contact, Blog, BlogCategory
from django.forms import ModelForm
from django.apps import apps
from taggit.forms import *

MyModel1 = apps.get_model('accounts', 'UserProfileInfo')


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'



class BlogForm(ModelForm):

    class Meta:
        model = Blog
        fields = ('category', 'title','snipit', 'img','img_alt', 'description','title_meta','description_meta','keywords_meta')
        exclude = ('author', 'blog_url')





class CategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ('category',)




class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = MyModel1
        fields = ('skills', 'bio', 'profile_pic')