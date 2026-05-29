from django.contrib import admin
from .models import Vehiculo, Repuesto, OrdenTrabajo, ChecklistOrden, RepuestoOrden, Compra, AlertaPreventiva

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'marca', 'modelo', 'estado')
    list_filter = ('estado', 'tipo', 'marca')
    search_fields = ('placa', 'marca', 'modelo')

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'stock', 'stock_minimo', 'precio_unitario')
    list_filter = ('stock',)
    search_fields = ('codigo', 'nombre')

class ChecklistOrdenInline(admin.StackedInline):
    model = ChecklistOrden
    can_delete = False

class RepuestoOrdenInline(admin.TabularInline):
    model = RepuestoOrden
    extra = 1

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'vehiculo', 'tipo_mantenimiento', 'prioridad', 'estado', 'tecnico', 'fecha_creacion')
    list_filter = ('estado', 'prioridad', 'tipo_mantenimiento', 'fecha_creacion')
    search_fields = ('codigo', 'vehiculo__numero_economico', 'tecnico__username')
    inlines = [ChecklistOrdenInline, RepuestoOrdenInline]
    readonly_fields = ('fecha_creacion', 'codigo')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'proveedor', 'fecha_compra', 'monto')
    list_filter = ('fecha_compra', 'proveedor')
    search_fields = ('numero_factura', 'proveedor', 'descripcion')

@admin.register(AlertaPreventiva)
class AlertaPreventivaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'tipo_alerta', 'intervalo_horas', 'intervalo_km', 'activa')
    list_filter = ('activa', 'tipo_alerta')
    search_fields = ('vehiculo__numero_economico', 'tipo_alerta')
