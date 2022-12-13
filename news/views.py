from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Blog, Contact, BlogCategory,Subscribe
from django.contrib.auth.models import User
from django.apps import apps
MyModel1 = apps.get_model('accounts', 'UserProfileInfo')
from .forms import ContactForm, BlogForm, forms,UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .filters import *
from django.core.paginator import Paginator
from gtts import gTTS
MyModel1 = apps.get_model('accounts', 'UserProfileInfo')
from bs4 import BeautifulSoup
from django.http import JsonResponse




# Create your views here.

def index(request):
    blog = Blog.objects.filter().order_by('-created')
    paginator = Paginator(blog, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    blog_category = BlogCategory.objects.filter().order_by('-created')[:4]
    return render(request, 'main/index.html', {'blog': page_obj, 'blog_category': blog_category})


def about(request):
    return render(request, 'main/about.html',)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('index')
        else:
            messages.info(request, 'fill valid data')
    form = ContactForm()
    context = {'form': form}

    return render(request, 'main/contact.html', context)


# this is for blog details page
def blog(request):
    blog = Blog.objects.filter().order_by('-created')
    return render(request, 'main/blog.html', {'blog': blog})

def Blogdetails(request, url):
    blogdetail = Blog.objects.filter(blog_url=url)
    blog = Blog.objects.filter().order_by('-created')[:3]
    return render(request, 'main/blog-single.html', {'blogdata': blogdetail, 'blog': blog})


def categories(request):
    cat_data = BlogCategory.objects.filter().order_by('-created')
    return render(request, 'main/categories.html', { 'categories': cat_data})



def category_details(request, url):
    category = BlogCategory.objects.filter(slug=url)
    cat = BlogCategory.objects.filter(slug=url).values_list('id', flat=True)

    cate = list(cat)
    data = cate[0]

    blog = Blog.objects.filter(category_id=data).order_by('-created')[:10]
    # print('catdata',cat)
    context = {'category': category, 'blog': blog}

    return render(request, 'main/category-single.html', context)
# admin for users

@login_required(login_url="/accounts/login")
def profile(request):
    data = MyModel1.objects.filter(user=request.user).first()

    if request.method == 'POST':

        form = UserProfileInfoForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('profile')



    form = UserProfileInfoForm(instance=data)
    # form = BlogForm()
    blog_count = Blog.objects.filter(author=request.user).count()
    instance = Blog.objects.filter(author=request.user).order_by('-created')
    return render(request, 'main/profile.html', { 'form': form, 'instance': instance , 'count': blog_count })

@login_required(login_url="/accounts/login")
def add_blog(request):
    if request.method == 'POST':

        form = BlogForm(request.POST, request.FILES)
        title = request.POST['title']
        des = request.POST['description']
        des = BeautifulSoup(des)
        t = des.getText()
        print(t)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user



            mytexts = (f' blog title is {title} and details is {t}')
            print(mytexts)


            language = 'en'
            myobj = gTTS(text=mytexts, lang=language, slow=False)
            music = myobj.save(f'media/audio/{title}.mp3')

            instance.save()
            messages.info(request, 'blog uploaded')
            return redirect('profile')

    form = BlogForm()
    instance = Blog.objects.filter(author=request.user).order_by('-created')
    return render(request, 'main/add_blog.html', {'form': form, 'instance': instance})

# for delete blog posts
def delete(request, id):
    data = Blog.objects.get(id=id)
    data.delete()
    messages.info(request, 'blog deleted successfully')
    return redirect('/profile')

# for delete blog posts
def update(request, id):
    data = Blog.objects.get(id=id)

    if request.method == 'POST':

        form = BlogForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = BlogForm(instance=data)
    return render(request, 'main/add_blog.html', {'form': form})


""" this search bar based on api  """
def search(request):
    address = request.GET.get('address')

    payload = []
    if address:
        data = Blog.objects.filter(title__icontains=address)


        for data in data:
            payload.append(data.blog_url)

    return JsonResponse({'status': 200, 'data': payload})






def profile_update(request, id):
    data = MyModel1.objects.filter(id=id).first()
    print(data)

    if request.method == 'POST':

        form = UserProfileInfoForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = UserProfileInfoForm(instance=data)
    return render(request, 'profile.html', {'form': form})

def author(request):
    author = MyModel1.objects.all()
    return render(request, 'main/authors.html', {'author': author})

def author_details(request, id):
    author_data = MyModel1.objects.filter(id=id)
    return render(request, 'main/author-single.html', {'author_data': author_data})



def subscribe(request):

    if request.method == 'POST':

        email = request.POST['email']

        if Subscribe.objects.filter(email=email).exists():
            messages.info('this email in already register')

        else:
            data = Subscribe.objects.create(email=email)
            data.save()
            messages.info('submit successfully')
            return redirect('index')


"""this is for 404 page """
def error_404_view(request, exception):
    return render(request, 'main/404.html')


