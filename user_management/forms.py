from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserChangeForm
from django.contrib.auth.models import Group

from user_management.models import User

# Register your models here.


class CustomUserCreationForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label="Privileges (Groups)"
    )

    class Meta:
        model = User
        fields = ["employee_id", "first_name", "last_name", "role", "unit", "groups"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password("Audit@HMIL")
        if commit:
            user.save()
            # Save many-to-many data (groups)
            self.save_m2m()
        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["employee_id", "first_name", "last_name", "role", "unit", "groups"]

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label="Privileges (Groups)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["employee_id"].disabled = True


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]


class PrivilegeForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
