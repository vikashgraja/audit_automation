from django.forms import ModelForm
from .models import redflags

import django.forms as forms

class RedFlagForm(ModelForm):
    class Meta:
        model = redflags
        fields = ['name', 'description', 'assigned_to']

        assigned_to = forms.ModelChoiceField(queryset=redflags.objects.all(), empty_label="Select Auditor",
                                            widget=forms.Select(attrs={
                                                'class': "form-select text-center fw-bold",
                                                'style': 'max-width: auto;',
                                            }))

        # manual = forms.FileInput()
