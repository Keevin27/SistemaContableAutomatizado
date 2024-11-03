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
    nombre = models.CharField(max_length=100, default='')
    nominal = models.DecimalField(max_digits=10, decimal_places=2)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    puesto = models.CharField(max_length=100)
    vacaciones = models.DecimalField(max_digits=5, decimal_places=2)
    septimo = models.DecimalField(max_digits=10, decimal_places=2)
    isss = models.DecimalField(max_digits=10, decimal_places=2)
    afp = models.DecimalField(max_digits=10, decimal_places=2)
    insaforp = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    costo_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    aguinaldo = models.DecimalField(max_digits=10, decimal_places=2)
    anios = models.IntegerField(default=1)
    factor_recargo = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    factor_recargo_con_eficiencia = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return self.nombre

class OrdenDeDesarrollo(models.Model):
    mod = models.DecimalField(max_digits=10, decimal_places=2)
    moi = models.DecimalField(max_digits=10, decimal_places=2)
    moh = models.DecimalField(max_digits=10, decimal_places=2)
    cif = models.DecimalField(max_digits=10, decimal_places=2)
    total_cif = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_cif = models.DecimalField(max_digits=10, decimal_places=2)
    total_loc = models.DecimalField(max_digits=10, decimal_places=2)
    costo_por_linea = models.DecimalField(max_digits=10, decimal_places=2)
    lineas_mes = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    costo_producto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

class Modulo(models.Model):
    orden_desarrollo = models.ForeignKey(OrdenDeDesarrollo, on_delete=models.CASCADE, null= True)
    nombre_modulo = models.CharField(max_length=100, default='')
    descripcion = models.CharField(max_length=100, default='')
    optimista = models.IntegerField()
    probable = models.IntegerField()
    pesimista = models.IntegerField()
    lineas_esperadas = models.IntegerField()
    costo_modulo = models.DecimalField(max_digits=10, decimal_places=2)

class Asignacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    orden = models.ForeignKey(OrdenDeDesarrollo, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completado', 'Completado')])

