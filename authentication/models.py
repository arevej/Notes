from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User)
    coord_x = models.IntegerField(default = 0)
    coord_y = models.IntegerField(default = 0)
    color = models.CharField(max_length=200, default= 'blue')
    width = models.IntegerField(default = 100)
    height = models.IntegerField(default = 100)
    text = models.CharField(max_length=1000000)
