from django.db import models


# Create your models here.


class redflags(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    username = models.CharField(max_length=30)
    userid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    manuals = models.FileField(upload_to='manuals/')
