from datetime import date
from django.shortcuts import render, redirect
from .models import Cuenta,Transaccion
# Create your views here.
def home(request):
    return render(request, 'home.html')
def catalogoDeCuentas(request):
    cuentas = Cuenta.objects.all()
    return render(request, 'catalogoDeCuentas.html', {'cuentas': cuentas})
def transacciones(request):
    if request.method=='GET':
        transacciones = Transaccion.objects.all()
        return render(request, 'transaccion.html', {'transaccion': transacciones})
    else:
        cuentaCargar= request.POST['cuentaCargar']
        montoCargar= request.POST.get('montoCargar')
        cuentaAbonar = request.POST['cuentaAbonar']
        montoAbonar = request.POST.get('montoAbonar')
        descripcion = request.POST.get('descripcion')
        iva = request.POST('agregarIVA')
       

        if iva == False:
            transacciones=Transaccion(cuentaCargar=cuentaCargar,montoCargar=montoCargar,cuentaAbonar=cuentaAbonar,montoAbonar=montoAbonar,descripcion=descripcion)
            transacciones.save()
    return redirect('librodiario/')



        
    
    