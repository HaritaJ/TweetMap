from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    searchStr=models.CharField(max_length=32)