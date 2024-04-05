from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import UserCreationForm
from .models import User


@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, 'User_management/user_list.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def register_user(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()

        #     username = request.POST.get('username')
        #     email = request.POST.get('email')
        #     first_name = request.POST.get('first_name')
        #     last_name = request.POST.get('last_name')
        #     password = request.POST.get('password')
        #     is_admin = request.POST.get('Admin')
        #     if not request.GET.get('Admin', None) == None:
        #         print(is_admin)
        #
        # # Check if a user with the provided username already exists
        #     user = User.objects.filter(username=username)
        #
        #     if user.exists():
        #     # Display an information message if the username is taken
        #     # messages.info(request, "Username already taken!")
        #         return redirect('/register/')
        #
        # # Create a new User object with the provided information
        #     user = User.objects.create_user(
        #         first_name=first_name,
        #         last_name=last_name,
        #         username=username,
        #         email=email
        #     )
        #
        # # Set the user's password and save the user object
        #     user.set_password(password)
        #     user.save()
        #
        # # Display an information message indicating successful account creation
        # # messages.info(request, "Auditor created Successfully!")
            return redirect('/register/')
    else:
        form = UserCreationForm()

    # Render the registration page template (GET request)
    return render(request, 'User_management/create_user.html',{'form': form})


@user_passes_test(lambda u: u.is_superuser)
def deleteuser(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect("user_list")

@user_passes_test(lambda u: u.is_superuser)
def changeadmin(request, username):
    user = User.objects.get(username=username)
    if user.is_superuser == False:
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
    else:
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False
        user.save()
    return redirect("user_list")