from django.shortcuts import render, redirect
from .models import *
from .forms import *
from decimal import Decimal
from django.db.models import Case, When, Value
from datetime import date
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')
def catalogoDeCuentas(request):
    cuentas = Cuenta.objects.all().order_by(
            Case(
                When(clasificacion='Activo corriente', then=Value(1)),
                When(clasificacion='Activo no corriente', then=Value(2)),
                When(clasificacion='Pasivo corriente', then=Value(3)),
                When(clasificacion='Pasivo no corriente', then=Value(4)),
                When(clasificacion='Patrimonio', then=Value(4)),
                When(clasificacion='Gastos', then=Value(5)),
                When(clasificacion='Ingresos', then=Value(6)),
                When(clasificacion='Cierre', then=Value(7)),
            )
        )
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
    elif clasificacion == 'Cierre':
        total = Cuenta.objects.filter(clasificacion='Cierre').count() + 1
        totalstr = str(total).zfill(2)
        codigo = f"61{totalstr}"
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

def estadosFinancieros(request):
    if request.method == 'GET':
        cuentas = Cuenta.objects.all().order_by(
            Case(
                When(clasificacion='Activo corriente', then=Value(1)),
                When(clasificacion='Activo no corriente', then=Value(2)),
                When(clasificacion='Pasivo corriente', then=Value(3)),
                When(clasificacion='Pasivo no corriente', then=Value(4)),
                When(clasificacion='Patrimonio', then=Value(4)),
                When(clasificacion='Gastos', then=Value(5)),
                When(clasificacion='Ingresos', then=Value(6)),
                When(clasificacion='Cierre', then=Value(7)),
            )
        )
        try:
            periodos = Periodo.objects.all()
        except Periodo.DoesNotExist:
            periodos = None  
        
        return render(request, 'estadosFinancieros.html', {'cuentas': cuentas, 'periodos': periodos})
    else:
        periodo = nuevo_periodo()
        datos = json.loads(request.body)
        periodo.aReinvertir = datos.get('utilidadInvertida', 0)
        periodo.save()
        try:
            cuentaCapital = Cuenta.objects.get(nombre='Capital')
        except Cuenta.DoesNotExist:
            cod = generar_codigo('Patrimonio')
            cuentaCapital = Cuenta.objects.create(nombre = 'Capital', codigo = cod, clasificacion='Patrimonio')
        try:
            cuentaCapitalNoInvertido = Cuenta.objects.get(nombre='Capital no invertido')
        except Cuenta.DoesNotExist:
            cod = generar_codigo('Cierre')
            cuentaCapitalNoInvertido = Cuenta.objects.create(nombre = 'Capital no invertido', codigo = cod, clasificacion='Cierre')
        cuentaCapital.haber = datos.get('cuentaCapitalH', 0)
        cuentaCapital.debe = datos.get('cuentaCapitalD', 0)
        cuentaCapital.save()
        cuentaCapitalNoInvertido.haber += datos.get('noReinvertido', 0)
        cuentaCapitalNoInvertido.save()
        print('hasta aqui')
        for cuenta_recibida in datos.get('cuentas', []):
            cuenta = Cuenta.objects.get(codigo = cuenta_recibida['id'])
            CuentaPeriodica.objects.create(
                codigo = cuenta.codigo,
                periodo = periodo,
                nombre = cuenta.nombre,
                debe = cuenta_recibida.get('debe', 0),
                haber = cuenta_recibida.get('haber', 0),
                ajusteDebe = cuenta_recibida.get('ajusteDebe', 0),
                ajusteHaber = cuenta_recibida.get('ajusteHaber', 0),
                estadoResultado = cuenta_recibida.get('resultadoCheckbox', False),
                estadoCapital = cuenta_recibida.get('capitalCheckbox', False),
            )
            cuenta.debe = cuenta_recibida.get('generalDebe', 0)
            cuenta.haber = cuenta_recibida.get('generalHaber', 0)
            if cuenta.nombre == 'Capital':
                cuenta.haber = datos.get('cuentaCapitalH', 0)
                cuenta.debe = datos.get('cuentaCapitalD', 0)
            if cuenta.nombre == 'Capital no invertido':
                cuenta.haber += datos.get('noReinvertido', 0)
            cuenta.save()
        return JsonResponse({'status': 'success'}, status=200)
    
def consultarEstadosFinancieros(request, numPeriodo):
    periodo = Periodo.objects.get(numero=numPeriodo)
    cuentas = CuentaPeriodica.objects.filter(periodo = periodo)
    periodos = Periodo.objects.all()
    return render(request, 'estadosFinancieros.html', {'cuentas': cuentas, 'periodos': periodos, 'consulta':True, 'period':periodo})

def nuevo_periodo():
    try:
        ultimoPeriodo = Periodo.objects.latest('numero')
        numeroPeriodo = ultimoPeriodo.numero + 1
    except Periodo.DoesNotExist:
        numeroPeriodo = 1
        ultimoPeriodo = None  
    if ultimoPeriodo != None:
        ultimoPeriodo.fecha_fin = date.today()
    fechaInicio = date.today()
    periodo = Periodo(numero = numeroPeriodo, fecha_inicio = fechaInicio)
    periodo.save()
    return periodo