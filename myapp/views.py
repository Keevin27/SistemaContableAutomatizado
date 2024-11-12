from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from decimal import Decimal
from django.db.models import Sum,Max
from django.db.models import Case, When, Value
from datetime import date
from django.http import JsonResponse
import json

from .models import Cuenta,Transaccion
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


def orden_de_desarrollo(request):

    return render(request)

@csrf_exempt
def control_de_costos(request):
    if request.method == 'POST':
        
        datos = json.loads(request.body.decode('utf-8'))
        orden = OrdenDeDesarrollo()
        
        costos = datos[0]
        print(costos)

        print(costos.get('mod'))
        orden.mod = Decimal(costos.get('mod'))
        orden.moi = Decimal(costos.get('moi'))
        orden.moh = Decimal(costos.get('moh'))
        orden.cif = Decimal(costos.get('cif'))
        orden.total_cif = Decimal(costos.get('total_cif'))
        orden.tasa_cif = Decimal(costos.get('tasa_cif'))
        orden.total_loc = Decimal(costos.get('total_loc'))
        orden.costo_por_linea = Decimal(costos.get('costo_por_linea'))
        orden.lineas_mes = Decimal(costos.get('lineas_mes'))
        orden.tiempo_estimado = Decimal(costos.get('tiempo_estimado'))
        orden.costo_producto = Decimal(costos.get('costo_producto'))
        orden.precio_venta = Decimal(costos.get('precio_venta'))
        orden.save()
        datos.pop(0)

        for dato in datos:
            modulo = Modulo()
            modulo.nombre_modulo = dato.get('nombre_modulo')
            modulo.descripcion = dato.get('descripcion')
            modulo.optimista = int(dato.get('optimista'))
            modulo.probable = int(dato.get('probable'))
            modulo.pesimista = int(dato.get('pesimista'))
            modulo.lineas_esperadas = int(dato.get('lineas_esperadas'))
            modulo.costo_modulo = Decimal(dato.get('costo_modulo'))
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

def transacciones(request):
    if request.method=='GET':
        transacciones = Transaccion.objects.all().order_by('fecha')
        cuentas = Cuenta.objects.all()
        total_debe = Transaccion.objects.aggregate(total_debe=Sum('montoDebe'))['total_debe'] or 0
        total_haber = Transaccion.objects.aggregate(total_haber=Sum('montoHaber'))['total_haber'] or 0

        return render(request, 'transaccion.html', {'transacciones': transacciones,'cuentas':cuentas,'total_debe': total_debe,'total_haber': total_haber})
    else:
        transacciones = Transaccion.objects.all().order_by('fecha')
        cuentas = Cuenta.objects.all()
        cuentaCargarID= request.POST.get('cuentaCargar')
        montoCargar= Decimal(request.POST.get('montoCargar',0))
        cuentaAbonarID = request.POST.get('cuentaAbonar')
        descripcion = request.POST.get('descripcion')
        iva = request.POST.get('agregarIVA','off')
        montoHaber=montoCargar

        try:
            ultima_transaccion = Transaccion.objects.latest('codigo')
            ultimo_codigo=ultima_transaccion.codigo
            nuevo_codigo = int(ultimo_codigo) + 1
        except:
            nuevo_codigo = '1'

        cuenta_cargar = Cuenta.objects.get(nombre=cuentaCargarID)
        cuenta_abonar = Cuenta.objects.get(nombre=cuentaAbonarID)

        if iva =='on':
            
            if cuenta_abonar.clasificacion == 'Activo corriente':
                cuenta_iva = Cuenta.objects.get(nombre='IVA credito fiscal')
                montoIVA = montoHaber*Decimal(0.13)
                montoHaber=montoHaber+montoIVA
                transacciones_iva=Transaccion(codigo=nuevo_codigo,debe=cuenta_iva.nombre,montoDebe=montoIVA,descripcion=descripcion,montoHaber=0)
                transacciones_iva.save()
                cuenta_iva.debe = (cuenta_iva.debe or Decimal('0')) + montoIVA
                cuenta_iva.save()
            else:
                cuenta_iva = Cuenta.objects.get(nombre='IVA debito fiscal')
                montoIVA = montoCargar*Decimal(0.13)
                montoCargar=montoCargar+montoIVA
                transacciones_iva=Transaccion(codigo=nuevo_codigo,haber=cuenta_iva.nombre,montoDebe=0,descripcion=descripcion,montoHaber=montoIVA)
                transacciones_iva.save()
                cuenta_iva.haber = (cuenta_iva.haber or Decimal('0')) + montoIVA
                cuenta_iva.save()

        cuentas = Cuenta(nombre=cuentaCargarID)
        transacciones=Transaccion(codigo=nuevo_codigo,debe=cuentaCargarID,montoDebe=montoCargar,haber=cuentaAbonarID,montoHaber=montoHaber,descripcion=descripcion)
        transacciones.save()

        cuenta_cargar.debe = (cuenta_cargar.debe or 0) + montoCargar
        cuenta_cargar.save()

        cuenta_abonar.haber = (cuenta_abonar.haber or 0) + montoHaber
        cuenta_abonar.save()

    return redirect('librodiario')

def libroMayor(request):
    cuentas=Cuenta.objects.all()
    transacciones = []
    for cuenta in cuentas:
            if cuenta.debe > cuenta.haber:
                cuenta.diferencia = cuenta.debe - cuenta.haber  # Saldo positivo
            elif cuenta.haber > cuenta.debe:
                cuenta.diferencia = (cuenta.haber - cuenta.debe)  # Saldo negativo
            else:
                cuenta.diferencia = 0

    if request.method == 'POST':
        cuenta_nombre = request.POST.get('cuentaRevisar')
        transacciones = Transaccion.objects.filter(debe=cuenta_nombre) | Transaccion.objects.filter(haber=cuenta_nombre)
        

        for transaccion in transacciones:
            if transaccion.debe == cuenta_nombre:
                transaccion.tipo = 'debe'
            elif transaccion.haber == cuenta_nombre:
                transaccion.tipo = 'haber'
        
        for cuenta in cuentas:
            if cuenta.debe > cuenta.haber:
                cuenta.diferencia = cuenta.debe - cuenta.haber  # Saldo positivo
            elif cuenta.haber > cuenta.debe:
                cuenta.diferencia = (cuenta.haber - cuenta.debe)  # Saldo negativo
            else:
                cuenta.diferencia = 0  # Saldo cero

    return render(request, 'libroMayor.html', {
        'cuentas': cuentas,
        'transacciones': transacciones,
    })


        



        
    
    