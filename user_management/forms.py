from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user_management.models import User
# Register your models here.

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email",'first_name','last_name']

# class UserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ["username", "email", 'first_name', 'last_name']
