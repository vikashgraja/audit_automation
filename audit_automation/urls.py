"""
URL configuration for audit_automation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from interface import views as interface_views
from user_management import views as user_management_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("login/", interface_views.login_page, name="login"),
    path("logout/", interface_views.user_logout, name="logout"),
    path("", interface_views.home, name="home"),
    path("redflag/", interface_views.red_flag, name="redflag"),
    path("add_redflag/", interface_views.addredflag, name="add_redflag"),
    path("deleterf/<str:flag>", interface_views.delete_redflag, name="delete_rf"),
    path("editrf/<str:flag>", interface_views.edit_redflag, name="edit_rf"),
    path("automation/", interface_views.automate, name="automation"),
    path("learn/", interface_views.learn, name="learn"),
    path("register/", user_management_views.register_user, name="register"),
    path("user_list/", user_management_views.user_list, name="user_list"),
    path("edit_user/<int:employee_id>", user_management_views.edit_user, name="edit_user"),
    path("delete_user/<int:employee_id>", user_management_views.deleteuser, name="delete_user"),
    path("update_admin/<int:employee_id>", user_management_views.changeadmin, name="update_admin"),
    path("unauthorized/", user_management_views.unauthorized, name="unauthorized"),
    path(
        "password/",
        user_management_views.CustomPasswordChangeView.as_view(template_name="login/password_change.html"),
        name="password",
    ),
    path(
        "password/done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="login/password_change_done.html"),
        name="password_change_done",
    ),
    path("download_manual/<str:flag>/", interface_views.download_manual, name="download_manual"),
    path("redflag/info/<str:flag_id>/", interface_views.redflag_info, name="redflag_info"),
    path("redflag/report/<str:flag_id>/", interface_views.redflag_report, name="redflag_report"),
]
