from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib import messages

@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
def user_list(request):
    users = User.objects.all()
    return render(request, 'User_management/user_list.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
def register_user(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print('formed')
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            # messages.success(request, 'User registered successfully')
            return redirect('user_list')
    else:
        form = UserCreationForm()
    
    # Create a mapping of unit IDs to their types for JavaScript filtering
    from .models import Unit
    import json
    units = Unit.objects.all()
    unit_types = {u.id: u.unit_type for u in units}

    # Render the registration page template (GET request)
    return render(request, 'User_management/create_user.html', {
        'form': form,
        'unit_types_json': json.dumps(unit_types)
    })


@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
def deleteuser(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect("user_list")

@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
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


@user_passes_test(lambda u: u.is_superuser, login_url='/unauthorized/')
def edit_user(request, username):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            return redirect('user_list')
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'User_management/update_user.html', {'form': form})

def unauthorized(request):
    return render(request, 'User_management/403.html')