from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vehiculo, OrdenTrabajo, Compra, Repuesto, ChecklistOrden, RepuestoOrden, MovimientoInventario

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.DateInput) or 'fecha' in field_name:
                field.widget.attrs['class'] = 'form-control'
                field.widget.input_type = 'date'
            else:
                field.widget.attrs['class'] = 'form-control'

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        exclude = ['codigo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'reporte_trabajos': forms.Textarea(attrs={'rows': 4}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'fecha_completada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'documento_adjunto': forms.FileInput(attrs={'class': 'form-control'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vehiculo_destino': forms.Select(attrs={'class': 'form-select'}),
            'repuesto_abastecido': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_repuesto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MovimientoManualForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['repuesto', 'tipo_movimiento', 'cantidad', 'observaciones']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = ChecklistOrden
        exclude = ['orden']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
                field.widget.attrs['style'] = 'width: 1.5rem; height: 1.5rem; cursor: pointer;'
            else:
                field.widget.attrs['class'] = 'form-control'

class RepuestoOrdenForm(forms.ModelForm):
    class Meta:
        model = RepuestoOrden
        fields = ['repuesto', 'cantidad']

class UsuarioForm(UserCreationForm):
    ROLES = [
        ('TECNICO', 'Técnico (Solo Móvil)'),
        ('ADMIN', 'Administrador (Acceso Total)'),
    ]
    rol = forms.ChoiceField(choices=ROLES, required=True, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-control'
        
        # Set initial value based on instance
        if self.instance and self.instance.pk:
            if self.instance.is_superuser or self.instance.is_staff:
                self.initial['rol'] = 'ADMIN'
            else:
                self.initial['rol'] = 'TECNICO'
