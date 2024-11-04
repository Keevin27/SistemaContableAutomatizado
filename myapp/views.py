from datetime import date
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from decimal import Decimal
from django.db.models import Sum,Max

from .models import Cuenta,Transaccion
# Create your views here.
def home(request):
    return render(request, 'home.html')
def catalogoDeCuentas(request):
    cuentas = Cuenta.objects.all()
    return render(request, 'catalogoDeCuentas.html', {'cuentas': cuentas})
def agregarCuenta(request):
    if request.method == 'GET':
        return render(request, 'agregarCuenta.html')
    else:
        try:
            nombre = request.POST['nombre']
            clasificacion = request.POST['clasificacion']
            codigo = generar_codigo(clasificacion)
            debe = 0
            haber = 0
            print (request.POST['nombre'])

            cuenta = Cuenta(codigo=codigo, nombre=nombre, clasificacion=clasificacion, debe=debe, haber=haber)
            cuenta.save()
            return redirect('catalogodecuentas')
        except:
            return render(request, 'agregarCuenta.html')


def generar_codigo(clasificacion):
    if clasificacion == 'Activo corriente':
        total = Cuenta.objects.filter(clasificacion='Activo corriente').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"11{totalstr}"
    elif clasificacion == 'Activo no corriente':
        total = Cuenta.objects.filter(clasificacion='Activo no corriente').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"12{totalstr}"
    elif clasificacion == 'Pasivo corriente':
        total = Cuenta.objects.filter(clasificacion='Pasivo corriente').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"21{totalstr}"
    elif clasificacion == 'Pasivo no corriente':
        total = Cuenta.objects.filter(clasificacion='Pasivo no corriente').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"22{totalstr}"
    elif clasificacion == 'Patrimonio':
        total = Cuenta.objects.filter(clasificacion='Patrimonio').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"31{totalstr}"
    elif clasificacion == 'Gastos':
        total = Cuenta.objects.filter(clasificacion='Gastos').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"41{totalstr}"
    elif clasificacion == 'Ingresos':
        total = Cuenta.objects.filter(clasificacion='Ingresos').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"51{totalstr}"
    return codigo

def costo_mano_obra(request):

    if request.method == 'POST':
        
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = Empleado()
            nominal = form.cleaned_data['nominal']
            vacaciones = (nominal * 15 + (Decimal(0.3) * nominal * 15))/52
            septimo = nominal * 2
            aguinaldo = (21 * nominal) / 52
            salario = nominal * 5 + septimo + aguinaldo + vacaciones
            isss = salario * Decimal(0.075)
            afp = salario * Decimal(0.08)
            costo = salario + isss + afp
            empleado.nombre = form.cleaned_data['nombre']
            empleado.puesto = form.cleaned_data['puesto']
            empleado.nominal = nominal
            empleado.vacaciones = vacaciones
            empleado.septimo = septimo
            empleado.aguinaldo = aguinaldo
            empleado.salario = salario
            empleado.isss = isss
            empleado.afp = afp
            empleado.insaforp = 0
            empleado.costo = costo
            empleado.save()
            return redirect('costo_mano_obra')  # Redirige a una lista de empleados o a donde prefieras obviamente :v
    else:
        form = EmpleadoForm()
    return render(request, 'costo_mano_obra.html', {'form': form, 'empleados': Empleado.objects.all()})

def eliminar_empleado(request):
    if request.method == 'POST':
        data = request.POST
        id = data['id']
        empleado = Empleado.objects.get(id = id)
        empleado.delete()
    return redirect('costo_mano_obra')

def transacciones(request):
    if request.method=='GET':
        transacciones = Transaccion.objects.all().order_by('-codigo')
        cuentas = Cuenta.objects.all()
        total_debe = Transaccion.objects.aggregate(total_debe=Sum('montoDebe'))['total_debe'] or 0
        total_haber = Transaccion.objects.aggregate(total_haber=Sum('montoHaber'))['total_haber'] or 0

        return render(request, 'transaccion.html', {'transacciones': transacciones,'cuentas':cuentas,'total_debe': total_debe,'total_haber': total_haber})
    else:
        transacciones = Transaccion.objects.all().order_by('-codigo')
        cuentas = Cuenta.objects.all()
        cuentaCargarID= request.POST.get('cuentaCargar')
        montoCargar= Decimal(request.POST.get('montoCargar',0))
        cuentaAbonarID = request.POST.get('cuentaAbonar')
        descripcion = request.POST.get('descripcion')
        iva = request.POST.get('agregarIVA','off')
        montoHaber=montoCargar

        ultimo_codigo = Transaccion.objects.order_by('codigo').last()
        if ultimo_codigo is None:
            nuevo_codigo = 1 
        else:
            nuevo_codigo = int(ultimo_codigo.codigo) + 1 

        cuenta_cargar = Cuenta.objects.get(nombre=cuentaCargarID)
        cuenta_abonar = Cuenta.objects.get(nombre=cuentaAbonarID)

        if iva =='on':
            
            if cuenta_abonar.clasificacion == 'Activo corriente':
                cuenta_iva = Cuenta.objects.get(nombre='IVA credito fiscal')
                montoIVA = montoHaber*Decimal(0.13)
                montoHaber=montoHaber+montoIVA
                transacciones=Transaccion(codigo=nuevo_codigo,debe=cuenta_iva.nombre,montoDebe=montoIVA,descripcion=descripcion,montoHaber=0)
                transacciones.save()
                cuenta_iva.debe = (cuenta_iva.debe or Decimal('0')) + montoIVA
                cuenta_iva.save()
            else:
                cuenta_iva = Cuenta.objects.get(nombre='IVA debito fiscal')
                montoIVA = montoCargar*Decimal(0.13)
                montoCargar=montoCargar+montoIVA
                transacciones=Transaccion(codigo=nuevo_codigo,haber=cuenta_iva.nombre,montoDebe=0,descripcion=descripcion,montoHaber=montoIVA)
                transacciones.save()
                cuenta_iva.haber = (cuenta_iva.haber or Decimal('0')) + montoIVA
                cuenta_iva.save()

        cuentas = Cuenta(nombre=cuentaCargarID)
        transacciones=Transaccion(codigo=nuevo_codigo,debe=cuentaCargarID,montoDebe=montoCargar,haber=cuentaAbonarID,montoHaber=montoHaber,descripcion=descripcion)
        transacciones.save()

        cuenta_cargar.debe = (cuenta_cargar.debe or 0) + montoCargar
        cuenta_cargar.save()

        cuenta_abonar.haber = (cuenta_abonar.haber or 0) + montoCargar
        cuenta_abonar.save()

    return redirect('librodiario')

def libroMayor(request):
    cuentas=Cuenta.objects.all()
    transacciones = []

    if request.method == 'POST':
        cuenta_nombre = request.POST.get('cuentaRevisar')
        transacciones = Transaccion.objects.filter(debe=cuenta_nombre) | Transaccion.objects.filter(haber=cuenta_nombre)

        for transaccion in transacciones:
            if transaccion.debe == cuenta_nombre:
                transaccion.tipo = 'debe'
            elif transaccion.haber == cuenta_nombre:
                transaccion.tipo = 'haber'

    return render(request, 'libroMayor.html', {
        'cuentas': cuentas,
        'transacciones': transacciones,
    })


        



        
    
    