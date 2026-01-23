import django.forms as forms
from django.forms import ModelForm

from user_management.models import User
from .models import Automation


class AutomationForm(ModelForm):
    class Meta:
        model = Automation
        fields = ["name", "category", "assigned_to", "manual"]
        choices = [("Red Flag", "Red Flag"), ("Exceptions", "Exceptions")]

        category = forms.ChoiceField(
            label="Category",
            widget=forms.RadioSelect(
                choices=choices,
                attrs={
                    "class": "form-select text-center fw-bold",
                    "style": "max-width: auto;",
                },
            ),
        )
        assigned_to = forms.ModelChoiceField(
            queryset=User.objects.filter(
                is_superuser=False
            ),  # Assuming logic: assign to auditors/users. Fixes the bug too.
            empty_label="Select Auditor",
            widget=forms.Select(
                attrs={
                    "class": "form-select text-center fw-bold",
                    "style": "max-width: auto;",
                }
            ),
        )
