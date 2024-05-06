from django.db import models
from user_management.models import User

# Create your models here.


class redflags(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    lastrun = models.DateTimeField(null=True, blank=True)
    manual = models.FileField(upload_to='manuals/',null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
