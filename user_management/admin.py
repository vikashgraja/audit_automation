from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user_management.models import User

# Register your models here.

# class UserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ("username", "email",)
#
# class UserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#
# class UserAdmin(UserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#     model = User
#
# admin.site.register(User, UserAdmin)