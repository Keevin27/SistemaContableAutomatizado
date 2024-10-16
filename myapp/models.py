from django.db import models

# Create your models here.
class Cuenta(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)
    debe = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    haber = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Transaccion(models.Model):
    codigo = models.CharField(max_length=6)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField()
    activo = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null= True)
    montoDebe = models.DecimalField(max_digits=10, decimal_places=2)
    pasivo = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null= True)
    montoHaber = models.DecimalField(max_digits=10, decimal_places=2)
