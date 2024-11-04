"""
URL configuration for sistemaContable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import *
from myapp.views import home, catalogoDeCuentas,transacciones,libroMayor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('catalogo_de_cuentas/', catalogoDeCuentas, name='catalogodecuentas'),
    path('catalogo_de_cuentas/agregar_cuenta/', agregarCuenta, name='agregarcuenta'),
    path('costo_mano_obra', costo_mano_obra, name='costo_mano_obra'),
    path('costo_mano_obra/actualizar_empleado', actualizar_empleado, name='actualizar_empleado'),
    path('costo_mano_obra/eliminar_empleado', eliminar_empleado, name='eliminar_empleado'),
    path('estados_financieros/', estadosFinancieros, name='estadosfinancieros'),
    path('estados_financieros/<int:numPeriodo>/', consultarEstadosFinancieros, name='consultarEstadosfinancieros'),
    path('control_de_costos', control_de_costos, name='control_de_costos'),
    path('get_empleados', get_empleados, name='get_empleados'),
    path('librodiario/', transacciones, name='librodiario'),
    path('libromayor/',libroMayor, name='libromayor')

]
