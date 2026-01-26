import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django_ratelimit.decorators import ratelimit

from interface.models import Automation, Tool
from .forms import AutomationForm

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
    # return redirect('automation')
    return render(request, "pages/home.html")


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")


@login_required(login_url="login")
def automation(request):
    user = request.user
    if user.is_superuser:
        items = Automation.objects.all()
    else:
        items = Automation.objects.filter(assigned_to=user)
    context = {"flags": items}
    return render(request, "pages/automation.html", context=context)


@login_required(login_url="login")
def tools(request):
    items = Tool.objects.all()
    return render(request, "pages/tools.html", {"tools": items})


@user_passes_test(lambda u: u.groups.filter(name="Site Admin").exists() or u.is_superuser, login_url="/unauthorized/")
def add_tool(request):
    if request.method == "POST":
        name = request.POST.get("name")
        url = request.POST.get("url")
        if name and url:
            Tool.objects.create(name=name, url=url, created_by=request.user)
            messages.success(request, "Tool added successfully.")
            return redirect("tools")
        else:
            messages.error(request, "Please provide both name and URL.")
    return render(request, "pages/create_tool.html")


@user_passes_test(lambda u: u.groups.filter(name="Site Admin").exists() or u.is_superuser, login_url="/unauthorized/")
def delete_tool(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    tool.delete()
    messages.success(request, "Tool deleted successfully.")
    return redirect("tools")


@login_required(login_url="login")
def learn(request):
    return render(request, "pages/learn.html")


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def add_automation(request):
    if request.method == "POST":
        form = AutomationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Automation added successfully.")
            return redirect("automation")
    else:
        form = AutomationForm()
    return render(request, "pages/create_automation.html", {"form": form})


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def delete_automation(request, item_id):
    item = get_object_or_404(Automation, id=item_id)
    item.delete()
    messages.success(request, "Automation deleted successfully.")
    return redirect("automation")


@user_passes_test(lambda u: u.is_superuser, login_url="/unauthorized/")
def edit_automation(request, item_id):
    item = get_object_or_404(Automation, id=item_id)

    if request.method == "POST":
        form = AutomationForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, "Automation updated successfully.")

            return redirect("automation")
    else:
        form = AutomationForm(instance=item)

    return render(request, "pages/edit_automation.html", {"form": form})


@login_required(login_url="login")
def download_manual(request, flag):
    item = get_object_or_404(Automation, id=flag)
    # Check if manual exists
    if not item.manual:
        messages.error(request, "No manual uploaded for this automation.")
        return redirect("automation")

    response = HttpResponse(item.manual, content_type="application/force-download")
    response["Content-Disposition"] = f'attachment; filename="{item.manual.name}"'
    return response


@login_required(login_url="login")
def automation_info(request, item_id):
    item = get_object_or_404(Automation, id=item_id)
    return render(request, "pages/automation_info.html", {"rf": item})


@login_required(login_url="login")
def automation_report(request, item_id):
    item = get_object_or_404(Automation, id=item_id)
    return render(request, "pages/automation_report.html", {"rf": item})
