from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from user_management.models import User
# Register your models here.

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", 'first_name', 'last_name', 'role', 'unit']

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", 'first_name', 'last_name', 'role', 'unit']


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']