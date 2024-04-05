from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth.models import User
from user_management.models import User
from django.contrib import messages


# from django.http import HttpResponse

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # messages.success(request, "Try again")
            return redirect("login")

    return render(request, "login/login.html")


@login_required(login_url='login')
def home(request):
    return render(request, "pages/home.html")


def user_logout(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("home")


@login_required(login_url='login')
def red_flag(request):
    return render(request, "pages/red_flag.html")


@login_required(login_url='login')
def automate(request):
    return render(request, "pages/automation.html")


@login_required(login_url='login')
def learn(request):
    return render(request, "pages/learn.html")


