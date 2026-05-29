from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, F
from django.utils import timezone
from functools import wraps
from .models import Vehiculo, OrdenTrabajo, Compra, Repuesto, AlertaPreventiva, ChecklistOrden, RepuestoOrden, MovimientoInventario
from .forms import VehiculoForm, OrdenTrabajoForm, CompraForm, ChecklistForm, UsuarioForm, RepuestoForm, MovimientoManualForm

def admin_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('mobile_mis_ordenes')
        return view_func(request, *args, **kwargs)
    return wrapper

# --- VISTAS DE ESCRITORIO (ADMINISTRADOR) ---

def custom_logout(request):
    logout(request)
    return redirect('login')

@admin_required
def dashboard(request):
    # KPIs basicos
    vehiculos_total = Vehiculo.objects.count()
    vehiculos_mantenimiento = Vehiculo.objects.filter(estado='MANTENIMIENTO').count()
    ordenes_pendientes = OrdenTrabajo.objects.exclude(estado__in=['COMPLETADA', 'CANCELADA']).count()
    compras_mes = Compra.objects.filter(fecha_compra__month=timezone.now().month).aggregate(Sum('monto'))['monto__sum'] or 0
    
    alertas = AlertaPreventiva.objects.filter(activa=True)
    alertas_activas = [a for a in alertas if a.due_soon()]

    # Para graficos
    tipos_ot = OrdenTrabajo.objects.values('tipo_mantenimiento').annotate(total=Count('id'))
    tipos_labels = [item['tipo_mantenimiento'] for item in tipos_ot]
    tipos_data = [item['total'] for item in tipos_ot]

    context = {
        'vehiculos_total': vehiculos_total,
        'vehiculos_mantenimiento': vehiculos_mantenimiento,
        'ordenes_pendientes': ordenes_pendientes,
        'compras_mes': compras_mes,
        'alertas_activas': alertas_activas,
        'tipos_labels': tipos_labels,
        'tipos_data': tipos_data,
    }
    return render(request, 'dashboard.html', context)

@admin_required
def vehiculo_lista(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/lista.html', {'vehiculos': vehiculos})

@admin_required
def vehiculo_crear(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo creado exitosamente.")
            return redirect('vehiculo_lista')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculos/form.html', {'form': form, 'titulo': 'Nuevo Vehículo'})

@admin_required
def vehiculo_detalle(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    campos = [(f.verbose_name.title(), getattr(vehiculo, f.name)) for f in vehiculo._meta.fields if f.name != 'id']
    return render(request, 'generic_detalle.html', {
        'titulo': f'Vehículo: {vehiculo.placa}',
        'objeto': vehiculo,
        'campos': campos,
        'url_editar': 'vehiculo_editar',
        'url_volver': 'vehiculo_lista'
    })

@admin_required
def vehiculo_editar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado exitosamente.')
            return redirect('vehiculo_lista')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculos/form.html', {'form': form, 'titulo': f'Editar Vehículo: {vehiculo.placa}'})

@admin_required
def vehiculo_eliminar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado exitosamente.')
        return redirect('vehiculo_lista')
    return render(request, 'confirmar_eliminar.html', {'objeto': vehiculo, 'titulo': 'Eliminar Vehículo', 'url_cancelar': 'vehiculo_lista'})

@admin_required
def orden_lista(request):
    ordenes = OrdenTrabajo.objects.all().order_by('-fecha_creacion')
    return render(request, 'ordenes/lista.html', {'ordenes': ordenes})

@admin_required
def orden_crear(request):
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST)
        checklist = ChecklistForm(request.POST)
        if form.is_valid() and checklist.is_valid():
            orden = form.save()
            chk = checklist.save(commit=False)
            chk.orden = orden
            chk.save()
            messages.success(request, "Orden de trabajo creada.")
            return redirect('orden_lista')
    else:
        form = OrdenTrabajoForm()
        checklist = ChecklistForm()
    return render(request, 'ordenes/form.html', {'form': form, 'checklist': checklist, 'titulo': 'Nueva Orden de Trabajo'})

@admin_required
def orden_detalle(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    campos = [(f.verbose_name.title(), getattr(orden, f.name)) for f in orden._meta.fields if f.name != 'id']
    
    chk_obj, created = ChecklistOrden.objects.get_or_create(orden=orden)
    checklist_campos = [(f.verbose_name.title(), getattr(chk_obj, f.name)) for f in chk_obj._meta.fields if f.name not in ['id', 'orden']]
    
    repuestos_usados = orden.repuestos_usados.all()

    return render(request, 'generic_detalle.html', {
        'titulo': f'Orden de Trabajo: OT-{orden.codigo}',
        'objeto': orden,
        'campos': campos,
        'checklist_campos': checklist_campos,
        'repuestos_usados': repuestos_usados,
        'url_editar': 'orden_editar',
        'url_volver': 'orden_lista'
    })

@admin_required
def orden_editar(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    chk_obj, created = ChecklistOrden.objects.get_or_create(orden=orden)
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST, request.FILES, instance=orden)
        checklist = ChecklistForm(request.POST, instance=chk_obj)
        if form.is_valid() and checklist.is_valid():
            form.save()
            checklist.save()
            messages.success(request, 'Orden actualizada exitosamente.')
            return redirect('orden_lista')
    else:
        form = OrdenTrabajoForm(instance=orden)
        checklist = ChecklistForm(instance=chk_obj)
    return render(request, 'ordenes/form.html', {'form': form, 'checklist': checklist, 'titulo': f'Editar Orden: OT-{orden.codigo}'})

@admin_required
def orden_eliminar(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    if request.method == 'POST':
        orden.delete()
        messages.success(request, 'Orden eliminada exitosamente.')
        return redirect('orden_lista')
    return render(request, 'confirmar_eliminar.html', {'objeto': f'Orden de Trabajo OT-{orden.codigo}', 'titulo': 'Eliminar Orden', 'url_cancelar': 'orden_lista'})

@admin_required
def compra_lista(request):
    compras = Compra.objects.all().order_by('-fecha_compra')
    return render(request, 'compras/lista.html', {'compras': compras})

@admin_required
def compra_crear(request):
    if request.method == 'POST':
        form = CompraForm(request.POST, request.FILES)
        if form.is_valid():
            compra = form.save()
            # Logica para inventario
            if compra.repuesto_abastecido and compra.cantidad_repuesto:
                repuesto = compra.repuesto_abastecido
                repuesto.stock += compra.cantidad_repuesto
                repuesto.save()
                
                # Registrar en Kardex
                MovimientoInventario.objects.create(
                    repuesto=repuesto,
                    tipo_movimiento='ENTRADA',
                    cantidad=compra.cantidad_repuesto,
                    usuario=request.user,
                    origen_destino=f"Compra {compra.numero_factura or 'S/N'}",
                    observaciones=compra.descripcion
                )
                
            messages.success(request, "Compra registrada exitosamente.")
            return redirect('compra_lista')
    else:
        form = CompraForm()
    return render(request, 'generic_form.html', {'form': form, 'titulo': 'Registrar Compra'})

@admin_required
def compra_detalle(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    campos = [(f.verbose_name.title(), getattr(compra, f.name)) for f in compra._meta.fields if f.name != 'id']
    return render(request, 'generic_detalle.html', {
        'titulo': f"Compra: Factura {compra.numero_factura or 'S/N'}",
        'objeto': compra,
        'campos': campos,
        'url_editar': 'compra_editar',
        'url_volver': 'compra_lista'
    })

@admin_required
def compra_editar(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        form = CompraForm(request.POST, request.FILES, instance=compra)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compra actualizada exitosamente.')
            return redirect('compra_lista')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'generic_form.html', {'form': form, 'titulo': f"Editar Compra: Factura {compra.numero_factura or 'S/N'}"})

@admin_required
def compra_eliminar(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra eliminada exitosamente.')
        return redirect('compra_lista')
    return render(request, 'confirmar_eliminar.html', {'objeto': f"Compra {compra.numero_factura or 'S/N'} por S/{compra.monto}", 'titulo': 'Eliminar Compra', 'url_cancelar': 'compra_lista'})

# --- VISTAS DE LOGISTICA Y ALMACEN ---

@admin_required
def logistica_dashboard(request):
    total_repuestos = Repuesto.objects.count()
    bajo_stock = Repuesto.objects.filter(stock__lte=F('stock_minimo')).count()
    ultimos_movimientos = MovimientoInventario.objects.all().order_by('-fecha')[:10]
    
    return render(request, 'logistica/dashboard.html', {
        'total_repuestos': total_repuestos,
        'bajo_stock': bajo_stock,
        'ultimos_movimientos': ultimos_movimientos
    })

@admin_required
def kardex_lista(request):
    movimientos = MovimientoInventario.objects.all().order_by('-fecha')
    return render(request, 'logistica/kardex.html', {'movimientos': movimientos})

@admin_required
def movimiento_manual(request):
    if request.method == 'POST':
        form = MovimientoManualForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            mov.usuario = request.user
            mov.origen_destino = "Ajuste / Movimiento Manual"
            
            # Actualizar stock
            repuesto = mov.repuesto
            if mov.tipo_movimiento == 'ENTRADA':
                repuesto.stock += mov.cantidad
            else: # SALIDA o AJUSTE
                repuesto.stock -= mov.cantidad
            
            repuesto.save()
            mov.save()
            
            messages.success(request, f"Movimiento manual registrado. Nuevo stock de {repuesto.nombre}: {repuesto.stock}")
            return redirect('logistica_dashboard')
    else:
        form = MovimientoManualForm(initial={'tipo_movimiento': 'SALIDA'})
    return render(request, 'generic_form.html', {'form': form, 'titulo': 'Registrar Entrada / Salida Manual'})

@admin_required
def repuesto_lista(request):
    repuestos = Repuesto.objects.all().order_by('nombre')
    return render(request, 'repuestos/lista.html', {'repuestos': repuestos})

@admin_required
def repuesto_crear(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Repuesto registrado exitosamente.")
            return redirect('repuesto_lista')
    else:
        form = RepuestoForm()
    return render(request, 'generic_form.html', {'form': form, 'titulo': 'Nuevo Repuesto'})

@admin_required
def repuesto_detalle(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    campos = [(f.verbose_name.title(), getattr(repuesto, f.name)) for f in repuesto._meta.fields if f.name != 'id']
    return render(request, 'generic_detalle.html', {
        'titulo': f'Repuesto: {repuesto.codigo} - {repuesto.nombre}',
        'objeto': repuesto,
        'campos': campos,
        'url_editar': 'repuesto_editar',
        'url_volver': 'repuesto_lista'
    })

@admin_required
def repuesto_editar(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repuesto actualizado exitosamente.')
            return redirect('repuesto_lista')
    else:
        form = RepuestoForm(instance=repuesto)
    return render(request, 'generic_form.html', {'form': form, 'titulo': f'Editar Repuesto: {repuesto.codigo}'})

@admin_required
def repuesto_eliminar(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == 'POST':
        repuesto.delete()
        messages.success(request, 'Repuesto eliminado exitosamente.')
        return redirect('repuesto_lista')
    return render(request, 'confirmar_eliminar.html', {'objeto': f'Repuesto {repuesto.nombre}', 'titulo': 'Eliminar Repuesto', 'url_cancelar': 'repuesto_lista'})

# --- VISTAS DE USUARIOS ---

@admin_required
def usuario_lista(request):
    usuarios = User.objects.all().order_by('username')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@admin_required
def usuario_crear(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            rol = form.cleaned_data.get('rol')
            if rol == 'ADMIN':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()
            messages.success(request, "Técnico/Usuario creado exitosamente.")
            return redirect('usuario_lista')
    else:
        form = UsuarioForm()
    return render(request, 'generic_form.html', {'form': form, 'titulo': 'Nuevo Técnico / Usuario'})

@admin_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            rol = form.cleaned_data.get('rol')
            if rol == 'ADMIN':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()
            messages.success(request, 'Técnico/Usuario actualizado exitosamente.')
            return redirect('usuario_lista')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'generic_form.html', {'form': form, 'titulo': f'Editar Técnico: {usuario.username}'})

@admin_required
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Técnico/Usuario eliminado exitosamente.')
        return redirect('usuario_lista')
    return render(request, 'confirmar_eliminar.html', {'objeto': usuario.username, 'titulo': 'Eliminar Técnico/Usuario', 'url_cancelar': 'usuario_lista'})

# --- VISTAS MOVILES (TECNICOS) ---
from django.contrib.auth.views import LoginView

class MobileLoginView(LoginView):
    template_name = 'mobile/login.html'
    
    def get_success_url(self):
        return '/mobile/mis-ordenes/'

@login_required
def mobile_mis_ordenes(request):
    # Filtrar solo ordenes asignadas al tecnico logueado que no esten completadas
    ordenes = OrdenTrabajo.objects.filter(
        tecnico=request.user
    ).exclude(estado__in=['COMPLETADA', 'CANCELADA']).order_by('-fecha_creacion')
    return render(request, 'mobile/mis_ordenes.html', {'ordenes': ordenes})

@login_required
def mobile_reportar_orden(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk, tecnico=request.user)
    
    if request.method == 'GET' and orden.estado == 'CREADA':
        orden.estado = 'EN_PROCESO'
        orden.save()

    checklist, created = ChecklistOrden.objects.get_or_create(orden=orden)
    repuestos_disponibles = Repuesto.objects.filter(stock__gt=0)
    
    if request.method == 'POST':
        # Procesar checklist
        form_checklist = ChecklistForm(request.POST, instance=checklist)
        
        # Procesar estado y horas
        nuevo_estado = request.POST.get('estado')
        horas = request.POST.get('tiempo_trabajado')
        reporte = request.POST.get('reporte_trabajos')
        horometro = request.POST.get('horometro_registro')
        odometro = request.POST.get('odometro_registro')
        
        if form_checklist.is_valid():
            form_checklist.save()
            
            accion = request.POST.get('accion')
            
            if accion == 'completar':
                orden.estado = 'COMPLETADA'
            elif nuevo_estado:
                if nuevo_estado == 'CREADA':
                    orden.estado = 'EN_PROCESO'
                else:
                    orden.estado = nuevo_estado
            if horas:
                horas = horas.replace(',', '.')
                orden.tiempo_trabajado = horas
            if reporte:
                orden.reporte_trabajos = reporte
            if horometro:
                horometro = horometro.replace(',', '.')
                orden.horometro_registro = horometro
                # Opcional: Actualizar horometro actual del vehiculo si es mayor
                if float(horometro) > float(orden.vehiculo.horometro_actual):
                    orden.vehiculo.horometro_actual = horometro
                    orden.vehiculo.save()
            if odometro:
                odometro = odometro.replace(',', '.')
                orden.odometro_registro = odometro
                if float(odometro) > float(orden.vehiculo.odometro_actual):
                    orden.vehiculo.odometro_actual = odometro
                    orden.vehiculo.save()
                
            # Procesar repuestos agregados (formato: repuesto_id_X y cantidad_X)
            for key, value in request.POST.items():
                if key.startswith('repuesto_id_') and value:
                    rep_id = value
                    idx = key.split('_')[-1]
                    try:
                        cant = int(request.POST.get(f'cantidad_{idx}', 0))
                    except (ValueError, TypeError):
                        cant = 0
                    
                    if cant > 0:
                        rep = get_object_or_404(Repuesto, pk=rep_id)
                        if rep.stock >= cant:
                            RepuestoOrden.objects.create(orden=orden, repuesto=rep, cantidad=cant)
                            rep.stock -= cant
                            rep.save()
                            
                            # Registrar en Kardex
                            MovimientoInventario.objects.create(
                                repuesto=rep,
                                tipo_movimiento='SALIDA',
                                cantidad=cant,
                                usuario=request.user,
                                origen_destino=f"Orden OT-{orden.codigo} (Vehículo: {orden.vehiculo.placa})",
                                observaciones=f"Instalado por {request.user.username}"
                            )
                        else:
                            messages.error(request, f"Stock insuficiente para {rep.nombre}")

            orden.save()
            
            # Cambiar estado vehiculo si se completo la orden
            if orden.estado == 'COMPLETADA':
                orden.vehiculo.estado = 'DISPONIBLE'
                orden.vehiculo.save()
                orden.fecha_completada = timezone.now()
                orden.save()
                messages.success(request, "Orden completada exitosamente.")
                return redirect('mobile_mis_ordenes')
            else:
                messages.success(request, "Reporte actualizado.")
                return redirect('mobile_reportar_orden', pk=orden.pk)

    else:
        form_checklist = ChecklistForm(instance=checklist)

    estados_permitidos = [(v, l) for v, l in OrdenTrabajo.ESTADOS_ORDEN if v not in ['REV_CONFIRMADA', 'CREADA']]
    
    context = {
        'orden': orden,
        'tiempo_str': str(orden.tiempo_trabajado) if orden.tiempo_trabajado else '',
        'horometro_str': str(orden.horometro_registro) if orden.horometro_registro else '',
        'odometro_str': str(orden.odometro_registro) if orden.odometro_registro else '',
        'horometro_actual_str': str(orden.vehiculo.horometro_actual) if orden.vehiculo.horometro_actual else '',
        'odometro_actual_str': str(orden.vehiculo.odometro_actual) if orden.vehiculo.odometro_actual else '',
        'checklist': form_checklist,
        'repuestos_disponibles': repuestos_disponibles,
        'estados': estados_permitidos,
    }
    return render(request, 'mobile/reportar_orden.html', context)
