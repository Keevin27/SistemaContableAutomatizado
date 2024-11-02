from django import forms
from .models import *

class EmpleadoForm(forms.ModelForm):

    nombre = forms.CharField(label='Nombre', min_length=3, max_length=120, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del empleado','pattern':'[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+'}))
    puesto = forms.CharField(label='Puesto', min_length=3, max_length=120, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Puesto del empleado','pattern':'[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+'}))
    nominal = forms.DecimalField(label='Nominal', max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'$0.00'}))
    anios = forms.IntegerField(label='Años', min_value=0, max_value=100, required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1', 'step':'1'}))

    class Meta:
        model = Empleado
        fields = ['nombre', 'nominal', 'puesto', 'anios']

    def clean_nominal(self):
        anios = self.cleaned_data.get('anios')
        if anios <= 0:
            raise forms.ValidationError('Los años deben de ser un valor positivo.')
        return anios
    
    def clean_nominal(self):
        nominal = self.cleaned_data.get('nominal')
        if nominal <= 0:
            raise forms.ValidationError('El nominal debe ser un valor positivo.')
        return nominal

    def clean_salario(self):
        salario = self.cleaned_data.get('salario')
        if salario <= 0:
            raise forms.ValidationError('El salario debe ser un valor positivo.')
        return salario

    def clean_vacaciones(self):
        vacaciones = self.cleaned_data.get('vacaciones')
        if vacaciones < 0:
            raise forms.ValidationError('Las vacaciones no pueden ser un valor negativo.')
        return vacaciones

    def clean_aguinaldo(self):
        aguinaldo = self.cleaned_data.get('aguinaldo')
        if aguinaldo < 0:
            raise forms.ValidationError('El aguinaldo no puede ser un valor negativo.')
        return aguinaldo

    def clean_septimo(self):
        septimo = self.cleaned_data.get('septimo')
        if septimo < 0:
            raise forms.ValidationError('El séptimo no puede ser un valor negativo.')
        return septimo

    def clean_isss(self):
        isss = self.cleaned_data.get('isss')
        if isss < 0:
            raise forms.ValidationError('El ISSS no puede ser un valor negativo.')
        return isss

    def clean_afp(self):
        afp = self.cleaned_data.get('afp')
        if afp < 0:
            raise forms.ValidationError('El AFP no puede ser un valor negativo.')
        return afp

    def clean_insaforp(self):
        insaforp = self.cleaned_data.get('insaforp')
        if insaforp < 0:
            raise forms.ValidationError('El INSAFORP no puede ser un valor negativo.')
        return insaforp

    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        if costo < 0:
            raise forms.ValidationError('El costo no puede ser un valor negativo.')
        return costo

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['empleado', 'orden', 'estado']
