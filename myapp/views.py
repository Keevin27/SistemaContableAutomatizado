from django.shortcuts import render, redirect
from .models import *
from .forms import *
from decimal import Decimal

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
            septimo = nominal * 7
            anios = form.cleaned_data['anios']
            aguinaldo = 0

            if anios >= 1 and anios < 3 :
                aguinaldo = (15 * nominal) / 52
            if anios >= 3 and anios < 10:
                aguinaldo = (19 * nominal) / 52
            if anios > 10:
                aguinaldo = (19 * nominal) / 52

            salario = septimo + vacaciones # Salario cancelado

            isss = salario * Decimal(0.075)
            afp = salario * Decimal(0.08)
            insaforp = 0
            #salario +=  vacaciones

            costo = salario + vacaciones + isss + afp + insaforp

            empleado.nombre = form.cleaned_data['nombre']
            empleado.puesto = form.cleaned_data['puesto']
            empleado.nominal = nominal
            empleado.vacaciones = vacaciones
            empleado.septimo = septimo
            empleado.aguinaldo = aguinaldo
            empleado.salario = salario
            empleado.isss = isss
            empleado.afp = afp
            empleado.insaforp = insaforp
            empleado.costo = costo
            empleado.save()

            return redirect('costo_mano_obra')  # Redirige a una lista de empleados o a donde prefieras obviamente :v
    else:
        form = EmpleadoForm()
    return render(request, 'costo_mano_obra.html', {'form': form, 'empleados': Empleado.objects.all()})


def actualizar_empleado(request):

    if request.method == 'POST':

        form = EmpleadoForm(request.POST)

        if form.is_valid():
            data = request.POST
            id = data['id']
            empleado = Empleado.objects.get(id = id)
            
            nominal = form.cleaned_data['nominal']
            vacaciones = (nominal * 15 + (Decimal(0.3) * nominal * 15))/52
            septimo = nominal * 7
            anios = form.cleaned_data['anios']
            aguinaldo = 0
            
            if anios >= 1 and anios < 3 :
                aguinaldo = (15 * nominal) / 52
            if anios >= 3 and anios < 10:
                aguinaldo = (19 * nominal) / 52
            if anios > 10:
                aguinaldo = (19 * nominal) / 52

            salario = septimo + vacaciones # Salario cancelado

            isss = salario * Decimal(0.075)
            afp = salario * Decimal(0.08)
            insaforp = 0
            #salario +=  vacaciones

            costo = salario + vacaciones + isss + afp + insaforp

            empleado.nombre = form.cleaned_data['nombre']
            empleado.puesto = form.cleaned_data['puesto']
            empleado.nominal = nominal
            empleado.vacaciones = vacaciones
            empleado.septimo = septimo
            empleado.aguinaldo = aguinaldo
            empleado.salario = salario
            empleado.isss = isss
            empleado.afp = afp
            empleado.insaforp = insaforp
            empleado.costo = costo
            empleado.anios =  anios
            empleado.save()

            return redirect('costo_mano_obra')  # Redirige a una lista de empleados o a donde prefieras obviamente :v
        
        data = request.POST
        id = data['id']
        empleado = Empleado.objects.get(id = id)

    return render(request, 'actualizar_empleado.html', {'empleado': empleado})

def eliminar_empleado(request):
    if request.method == 'POST':
        data = request.POST
        id = data['id']
        empleado = Empleado.objects.get(id = id)
        empleado.delete()
    return redirect('costo_mano_obra')
