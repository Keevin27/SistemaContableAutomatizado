import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
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

            costo = salario + vacaciones + isss + afp + insaforp
            factor = costo / (nominal * 5)
            factor_eficiencia = factor / Decimal(0.85)
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
            empleado.factor_recargo = factor
            empleado.factor_recargo_con_eficiencia = factor_eficiencia
            empleado.costo_mensual = costo * 4
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

            costo = salario + vacaciones + isss + afp + insaforp
            factor = costo / (nominal * 5)
            factor_eficiencia = factor / Decimal(0.85)
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
            empleado.factor_recargo = factor
            empleado.factor_recargo_con_eficiencia = factor_eficiencia
            empleado.costo_mensual = costo * 4
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

def orden_de_desarrollo(request):

    return render(request)

def control_de_costos(request):
    
    if request.method == 'POST':
        
        datos = json.loads(request.body.decode('utf-8'))
        orden = OrdenDeDesarrollo()
        
        costos = datos[0]
        orden.mod = costos.get('mod')
        orden.moi = costos.get('moi')
        orden.moh = costos.get('moh')
        orden.cif = costos.get('cif')
        orden.total_cif = costos.get('total_cif')
        orden.tasa_cif = costos.get('tasa_cif')
        orden.total_loc = costos.get('total_loc')
        orden.costo_por_linea = costos.get('costo_por_linea')
        orden.lineas_mes = costos.get('lineas_mes')
        orden.tiempo_estimado = costos.get('tiempo_estimado')
        orden.costo_producto = costos.get('costo_producto')
        orden.precio_venta = costos.get('precio_venta')
        orden.save()
        datos.pop(0)

        for dato in datos:
            modulo = Modulo()
            modulo.nombre_modulo = dato.get('nombre_modulo')
            modulo.descripcion = dato.get('descripcion')
            modulo.optimista = dato.get('optimista')
            modulo.probable = dato.get('probable')
            modulo.pesimista = dato.get('pesimista')
            modulo.lineas_esperadas = dato.get('lineas_esperadas')
            modulo.costo_modulo = dato.get('costo_modulo')
            modulo.orden_desarrollo = orden
            modulo.save()

        #for dato in datos:
        return JsonResponse({'mensaje': 'Datos recibidos exitosamente'}, status=200)
    else:
        form = AsignacionForm()
    return render(request, 'control_de_costos.html', {'form': form, 'empleados': Empleado.objects.all()})

def get_empleados(request):
    if request.method == 'GET':
        empleados =  Empleado.objects.all().values('id','nombre','puesto','costo_mensual')
        lista_empleados = list(empleados)
        return JsonResponse(lista_empleados, safe = False)
    return JsonResponse(data = {'mensaje': 'No data', 'estado':'-1'})
