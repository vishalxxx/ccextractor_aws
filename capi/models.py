from django.db import models
import uuid
# Create your models here.


class Video(models.Model):
   # title = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    file = models.TextField()
    searched_key = models.TextField()








    
