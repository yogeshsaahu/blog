from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.apps import apps
MyModel1 = apps.get_model('accounts', 'UserProfileInfo')
from .forms import ContactForm, BlogForm,UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .filters import *
from django.core.paginator import Paginator
MyModel1 = apps.get_model('accounts', 'UserProfileInfo')
from django.http import JsonResponse
from taggit.models import Tag




"""this is for index page """
def index(request):
    blog = Blog.objects.filter().order_by('-created')
    paginator = Paginator(blog, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    blog_category = BlogCategory.objects.filter().order_by('-created')[:4]
    return render(request, 'main/index.html', {'blog': page_obj, 'blog_category': blog_category})



"""this is for about page """
def about(request):
    return render(request, 'main/about.html',)

"""this is for Privacy page """
def Privacy(request):
    return render(request, 'main/Privacy.html',)

"""this is for contact page """
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



"""this is for blog page """
def blog(request):
    blog = Blog.objects.filter().order_by('-created')
    return render(request, 'main/blog.html', {'blog': blog})

"""this is for blog details page """
def Blogdetails(request, url):
    blogdetail = Blog.objects.filter(blog_url=url)
    blog = Blog.objects.filter().order_by('-created')[:3]
    return render(request, 'main/blog-single.html', {'blogdata': blogdetail, 'blog': blog})



"""this is for tag page """
def post_list(request, tag_slug=None):
    posts = Blog.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'main/tag-single.html', {'posts': posts, 'tag': tag})




"""this is for category page """
def categories(request):
    # cat_data = BlogCategory.objects.filter().order_by('-created')
    count = BlogCategory.objects.annotate(num_comments=models.Count('blog')).all().order_by('-created')
    return render(request, 'main/categories.html', { "count": count})

"""this is for category details page """
def category_details(request, url):
    category = BlogCategory.objects.filter(slug=url)
    cat = BlogCategory.objects.filter(slug=url).values_list('id', flat=True)
    cate = list(cat)
    data = cate[0]
    blog = Blog.objects.filter(category_id=data).order_by('-created')[:10]
    context = {'category': category, 'blog': blog}
    return render(request, 'main/category-single.html', context)




""" this search bar based on api  """
def search(request):
    address = request.GET.get('address')
    payload = []
    if address:
        data = Blog.objects.filter(title__icontains=address)
        for data in data:
            payload.append(data.blog_url)
    return JsonResponse({'status': 200, 'data': payload})




"""this is for author page """
def author(request):
    author = MyModel1.objects.all()
    return render(request, 'main/authors.html', {'author': author})

"""this is for author details page """
def author_details(request, id):
    author_data = MyModel1.objects.filter(id=id)
    cat = MyModel1.objects.filter(id=id).values_list('id', flat=True)
    cate = list(cat)
    data = cate[0]
    blog = Blog.objects.filter(author_id=data).order_by('-created')[:10]
    context = {'author_data': author_data, 'blog': blog}
    return render(request, 'main/author-single.html', context)




"""this is for subscribe """
def subscribe(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        if Subscribe.objects.filter(email=email).exists():
            messages.info(request,'this email in already register')
            return redirect('index')
        else:
            data = Subscribe.objects.create(email=email, name=name)
            data.save()
            messages.info(request,'submit successfully')
            return redirect('index')




"""this is for 404 page """
def error_404_view(request, exception):
    return render(request, 'main/404.html')



# ''''''''''''''''''''''''''''user_admin''''''''''''''''''''''''''''''''''



"""this is for show user dashboard page """
@login_required(login_url="/accounts/login")
def user_dashboard(request):
    return render(request, "user_dash/dashboard.html")


"""this is for show user profile page """
@login_required(login_url="/accounts/login")
def user_profile(request):
    data = MyModel1.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = UserProfileInfoForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('user_profile')

    form = UserProfileInfoForm(instance=data)
    blog_count = Blog.objects.filter(author=request.user).count()


    return render(request, 'user_dash/user_profile.html', {'form': form, "blog_count": blog_count})


"""this is for update user profile page """
@login_required(login_url="/accounts/login")
def profile_update(request, id):
    data = MyModel1.objects.filter(id=id).first()

    if request.method == 'POST':

        form = UserProfileInfoForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileInfoForm(instance=data)
    return render(request, 'user_dash/user_profile.html', {'form': form})


"""this function for add new blog"""
@login_required(login_url="/accounts/login")
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            form.save_m2m()
            messages.info(request, 'blog uploaded')
            return redirect('user_blogs')

    form = BlogForm()
    instance = Blog.objects.filter(author=request.user).order_by('-created')
    return render(request, 'user_dash/add_blog.html', {'form': form, 'instance': instance})


"""this function for show user blogs"""
@login_required(login_url="/accounts/login")
def user_blogs(request):
    blog = Blog.objects.filter(author=request.user).order_by('-created')
    blog_count = Blog.objects.filter(author=request.user).count()
    return render(request, "user_dash/blog_list.html", {"blog": blog, "blog_count": blog_count})



"""this function for delete blog"""
@login_required(login_url="/accounts/login")
def delete(request, id):
    data = Blog.objects.get(id=id)
    data.delete()
    messages.info(request, 'blog deleted successfully')
    return redirect('user_blogs')


"""this function for update blog"""
@login_required(login_url="/accounts/login")
def update(request, id):
    data = Blog.objects.get(id=id)

    if request.method == 'POST':

        form = BlogForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('user_blogs')

    else:
        form = BlogForm(instance=data)
    return render(request, 'user_dash/add_blog.html', {'form': form})