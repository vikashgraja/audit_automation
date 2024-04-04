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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from interface.views import * #login_page, home, user_logout
from user_management.views import user_list

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', login_page, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    path('redflag/', red_flag, name ="redflag"),
    path('automation/', automate, name="automation"),
    path('learn/', learn, name="learn"),
    path('register/', register_user, name='register'),
    path('user_list/', user_list, name='user_list'),
    path('delete_user/', user_list, name='delete_user'),
    path('update_user/', user_list, name='update_user'),


    path("password/", auth_views.PasswordChangeView.as_view(template_name='login/password_change.html'),
         name='password'),
    path("password/done/", auth_views.PasswordChangeDoneView.as_view(template_name='login/password_change_done.html'),
         name='password_change_done'),


]
