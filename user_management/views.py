from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, UserChangeForm
from .models import Unit, User


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "login/password_change.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        # Update the user's flag
        self.request.user.password_change_required = False
        self.request.user.save()
        return super().form_valid(form)


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def user_list(request):
    users = User.objects.all()
    return render(request, "User_management/user_list.html", {"users": users})


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def register_user(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        print("formed")
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            messages.success(request, "User registered successfully")
            return redirect("user_list")
    else:
        form = CustomUserCreationForm()

    # Create a mapping of unit IDs to their types for JavaScript filtering
    import json

    units = Unit.objects.all()
    unit_types = {u.id: u.unit_type for u in units}

    # Render the registration page template (GET request)
    return render(
        request, "User_management/create_user.html", {"form": form, "unit_types_json": json.dumps(unit_types)}
    )


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def deleteuser(request, employee_id):
    user = get_object_or_404(User, employee_id=employee_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("user_list")


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def changeadmin(request, employee_id):
    user = User.objects.get(employee_id=employee_id)
    if user.is_superuser is not True:
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        messages.success(request, f"Admin privileges granted to {user.first_name}.")
    else:
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False
        user.save()
        messages.success(request, f"Privileges revoked for {user.first_name}.")
    return redirect("user_list")


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def edit_user(request, employee_id):
    user = User.objects.get(employee_id=employee_id)

    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")

            return redirect("user_list")
    else:
        form = UserChangeForm(instance=user)

    return render(request, "User_management/update_user.html", {"form": form})


def unauthorized(request):
    return render(request, "User_management/403.html")
