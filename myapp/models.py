from django.db import models

# Create your models here.
class Cuenta(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)