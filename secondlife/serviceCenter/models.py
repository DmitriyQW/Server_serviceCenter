from django.db import models

# Create your models here.

class Worker(models.Model):
    id = models.AutoField(primari_key=True)
    login = models.CharField(max_length=8)