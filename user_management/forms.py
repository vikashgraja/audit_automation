from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserChangeForm

from user_management.models import User

# Register your models here.


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["employee_id", "first_name", "last_name", "role", "unit"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password("Audit@HMIL")
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["employee_id", "first_name", "last_name", "role", "unit"]


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
