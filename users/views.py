from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UseRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
# Create your views here.

def registerView(request):
    if request.method == 'POST':
        form = UseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Akun dibuat untuk {username}!')
            return redirect('users:login')
    else:
        form = UseRegisterForm()

    context = {
        'Judul': 'SIGN UP',
        'form': form,
        'css': 'users/css/registration.css',
    }
    return render(request, 'users/register_base.html',context)

def loginView(request):
    context = {
        'Judul': 'LOGIN',
        'css': 'users/css/login.css',
    }
    user = None

    if request.method == "GET":
        if request.user.is_authenticated:
            #logika untuk user
            return redirect('index')
        else:
            #logika untuk anonym
            return render(request,'users/login_base.html', context)

    if request.method == "POST":

        username_login = request.POST['username']
        password_login = request.POST['password']

        user = authenticate(request, username=username_login, password=password_login)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Password/username salah!')
            return redirect('users:login')

@login_required
def logoutView(request):
    context = {
        'Judul': 'Logout',
    }

    if request.method == "POST":
        print(request.POST)
        if request.POST["logout"] == "Logout":
            logout(request)
            return redirect('index')

    return render(request, 'users/logout.html', context)