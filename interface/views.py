from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from user_management.models import User
from interface.models import redflags
from django.contrib import messages
from .forms import RedFlagForm


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
    user = request.user
    if user.is_superuser:
        flags = redflags.objects.all()
    else:
        flags = redflags.objects.filter(assigned_to=user)
    context = {'flags': flags}
    return render(request, "pages/red_flag.html", context=context)


@login_required(login_url='login')
def automate(request):
    return render(request, "pages/automation.html")


@login_required(login_url='login')
def learn(request):
    return render(request, "pages/learn.html")

@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
def addredflag(request):
    if request.method == "POST":
        form = RedFlagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add_redflag/')
    else:
        form = RedFlagForm()
    return render(request, 'pages/create_red_flag.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
def delete_redflag(request, flag):
    redflag = redflags.objects.get(id=flag)
    redflag.delete()
    return redirect("redflag")

@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
def edit_redflag(request, flag):
    redflag = redflags.objects.get(id=flag)

    if request.method == 'POST':
        form = RedFlagForm(request.POST, instance=redflag)

        if form.is_valid():
            form.save()

            return redirect('redflag')
    else:
        form = RedFlagForm(instance=redflag)

    return render(request, 'pages/edit_red_flag.html', {'form': form})
