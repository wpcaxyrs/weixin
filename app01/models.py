from django.db import models

# Create your models here.
class User_info(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)
    wx_id = models.CharField(max_length=32, null=True, blank=True)
