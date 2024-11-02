from django.db import models

# Create your models here.
class Cuenta(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50, null=True)
    debe = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    haber = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Transaccion(models.Model):
    codigo = models.CharField(max_length=6)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField()
    #activo = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null= True)
    activo = models.CharField(max_length=50)
    montoDebe = models.DecimalField(max_digits=10, decimal_places=2)
    #pasivo = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null= True)
    pasivo = models.CharField(max_length=50)
    montoHaber = models.DecimalField(max_digits=10, decimal_places=2)

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    nominal = models.DecimalField(max_digits=10, decimal_places=2)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    puesto = models.CharField(max_length=100)
    vacaciones = models.DecimalField(max_digits=5, decimal_places=2)
    septimo = models.DecimalField(max_digits=10, decimal_places=2)
    isss = models.DecimalField(max_digits=10, decimal_places=2)
    afp = models.DecimalField(max_digits=10, decimal_places=2)
    insaforp = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    aguinaldo = models.DecimalField(max_digits=10, decimal_places=2)
    anios = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre