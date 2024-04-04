from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
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


def register_user(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Auditor created Successfully!")
        return redirect('/register/')

    # Render the registration page template (GET request)
    return render(request, 'pages/register.html')