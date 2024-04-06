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
        print('formed')
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            return redirect('/register/')
    else:
        print("not ok")
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