import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django_ratelimit.decorators import ratelimit

from interface.models import redflags

from .forms import RedFlagForm

# Security logger
security_logger = logging.getLogger("django.security")


# Create your views here.


@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            security_logger.info(f"Successful login for user: {username}")
            if user.password_change_required:
                return redirect("password")
            return redirect("home")
        else:
            # Log failed login attempt
            security_logger.warning(
                f"Failed login attempt for username: {username} from IP: {request.META.get('REMOTE_ADDR')}"
            )
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("login")

    return render(request, "login/login.html")


@login_required(login_url="login")
def home(request):
    # return redirect('redflag')
    return render(request, "pages/home.html")


def user_logout(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("login")


@login_required(login_url="login")
def red_flag(request):
    user = request.user
    if user.is_superuser:
        flags = redflags.objects.all()
    else:
        flags = redflags.objects.filter(assigned_to=user)
    context = {"flags": flags}
    return render(request, "pages/red_flag.html", context=context)


@login_required(login_url="login")
def automate(request):
    return render(request, "pages/automation.html")


@login_required(login_url="login")
def learn(request):
    return render(request, "pages/learn.html")


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def addredflag(request):
    if request.method == "POST":
        form = RedFlagForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("redflag")
    else:
        form = RedFlagForm()
    return render(request, "pages/create_red_flag.html", {"form": form})


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def delete_redflag(request, flag):
    redflag = redflags.objects.get(id=flag)
    redflag.delete()
    return redirect("redflag")


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def edit_redflag(request, flag):
    redflag = redflags.objects.get(id=flag)

    if request.method == "POST":
        form = RedFlagForm(request.POST, request.FILES, instance=redflag)

        if form.is_valid():
            form.save()

            return redirect("redflag")
    else:
        form = RedFlagForm(instance=redflag)

    return render(request, "pages/edit_red_flag.html", {"form": form})


@login_required(login_url="login")
def download_manual(request, flag):
    redflag = redflags.objects.get(id=flag)
    response = HttpResponse(redflag.manual, content_type="application/force-download")
    response["Content-Disposition"] = f'attachment; filename="{redflag.manual.name}"'
    return response


@login_required(login_url="login")
def redflag_info(request, flag_id):
    rf = get_object_or_404(redflags, id=flag_id)
    return render(request, "pages/red_flag_info.html", {"rf": rf})


@login_required(login_url="login")
def redflag_report(request, flag_id):
    rf = get_object_or_404(redflags, id=flag_id)
    return render(request, "pages/red_flag_report.html", {"rf": rf})
