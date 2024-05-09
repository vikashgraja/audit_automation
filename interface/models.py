from django.db import models
from user_management.models import User

# Create your models here.


class redflags(models.Model):
    choices = [
        ("Red Flag", "Red Flag"),
        ("Audit Exceptions", "Audit Exceptions")
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30,choices=choices)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    lastrun = models.DateTimeField(null=True, blank=True)
    manual = models.FileField(upload_to='manuals/',null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
