from django.forms import ModelForm
from .models import redflags

import django.forms as forms

class RedFlagForm(ModelForm):
    class Meta:
        model = redflags
        fields = ['name', 'category', 'assigned_to', 'manual']
        choices = [
            ("Red Flag","Red Flag"),
            ("Exceptions","Exceptions")
        ]

        category = forms.ChoiceField(label='Category',widget=forms.RadioSelect(choices= choices,attrs={
                                                'class': "form-select text-center fw-bold",
                                                'style': 'max-width: auto;',
                                            }))
        assigned_to = forms.ModelChoiceField(queryset=redflags.objects.all(), empty_label="Select Auditor",
                                            widget=forms.Select(attrs={
                                                'class': "form-select text-center fw-bold",
                                                'style': 'max-width: auto;',
                                            }))

