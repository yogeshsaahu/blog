from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User, auth
from django.shortcuts import render

# Create your views here.
def register(request):
    if request.method == "POST":

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken. use different username')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email Taken. use different email ')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save();
                messages.info(request, 'user created')
                return redirect('/accounts/login')

        else:
            messages.info(request, 'password not matching..')
            return redirect('register')

        return redirect('/')

    else:
        return render(request, 'main/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            messages.info(request, 'you are login successfully')
            auth.login(request, user)
            return redirect('profile')

        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'main/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')