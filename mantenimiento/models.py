from django.db import models
from django.contrib.auth.models import User

class Vehiculo(models.Model):
    ESTADOS_VEHICULO = [
        ('DISPONIBLE', 'Disponible'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('FUERA_SERVICIO', 'Fuera de Servicio'),
    ]

    TIPOS_VEHICULO = [
        ('Excavadora', 'Excavadora'),
        ('Retroexcavadora', 'Retroexcavadora'),
        ('Cargador Frontal', 'Cargador Frontal'),
        ('Tractor sobre orugas', 'Tractor sobre orugas (Bulldozer)'),
        ('Motoniveladora', 'Motoniveladora'),
        ('Rodillo Compactador', 'Rodillo Compactador'),
        ('Minicargador', 'Minicargador'),
        ('Manipulador Telescópico', 'Manipulador Telescópico'),
        ('Camión Minero', 'Camión Minero'),
        ('Volquete', 'Volquete'),
        ('Tractocamión', 'Tractocamión'),
        ('Cama Baja', 'Cama Baja'),
        ('Camión Cisterna', 'Camión Cisterna (Agua/Combustible)'),
        ('Camión Grúa', 'Camión Grúa'),
        ('Hormigonera', 'Hormigonera (Trompo)'),
        ('Camioneta Pick-up', 'Camioneta Pick-up'),
        ('Furgoneta', 'Furgoneta'),
        ('Otro', 'Otro'),
    ]

    MARCAS_VEHICULO = [
        ('Caterpillar (CAT)', 'Caterpillar (CAT)'),
        ('Komatsu', 'Komatsu'),
        ('Volvo', 'Volvo'),
        ('Scania', 'Scania'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('FUSO', 'FUSO'),
        ('Hino', 'Hino'),
        ('Isuzu', 'Isuzu'),
        ('Mack', 'Mack'),
        ('Freightliner', 'Freightliner'),
        ('Kenworth', 'Kenworth'),
        ('Sany', 'Sany'),
        ('XCMG', 'XCMG'),
        ('LiuGong', 'LiuGong'),
        ('Liebherr', 'Liebherr'),
        ('Hyundai', 'Hyundai'),
        ('Toyota', 'Toyota'),
        ('Nissan', 'Nissan'),
        ('Ford', 'Ford'),
        ('Chevrolet', 'Chevrolet'),
        ('Otra', 'Otra (Especificar)'),
    ]

    placa = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="N° Placa")
    tipo = models.CharField(max_length=50, choices=TIPOS_VEHICULO, verbose_name="Tipo de Vehículo/Maquinaria")
    marca = models.CharField(max_length=50, choices=MARCAS_VEHICULO)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(verbose_name="Año Modelo")
    
    # Nuevos campos SUNARP
    placa_anterior = models.CharField(max_length=20, blank=True, null=True, verbose_name="Placa Anterior")
    numero_serie = models.CharField(max_length=50, blank=True, null=True, verbose_name="N° Serie")
    numero_vin = models.CharField(max_length=50, blank=True, null=True, verbose_name="N° VIN")
    numero_motor = models.CharField(max_length=50, blank=True, null=True, verbose_name="N° Motor")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color")
    propietarios = models.TextField(blank=True, null=True, help_text="Nombres de los propietarios")
    
    # Datos Técnicos Adicionales
    categoria = models.CharField(max_length=50, blank=True, null=True, verbose_name="Categoría")
    anio_fabricacion = models.IntegerField(blank=True, null=True, verbose_name="Año Fabricación")
    carroceria = models.CharField(max_length=50, blank=True, null=True, verbose_name="Carrocería")
    potencia = models.CharField(max_length=50, blank=True, null=True, verbose_name="Potencia")
    forma_rodaje = models.CharField(max_length=50, blank=True, null=True, verbose_name="Forma Rodaje")
    combustible = models.CharField(max_length=50, blank=True, null=True, verbose_name="Combustible")
    asientos = models.IntegerField(blank=True, null=True, verbose_name="Asientos")
    pasajeros = models.IntegerField(blank=True, null=True, verbose_name="Pasajeros")
    ruedas = models.IntegerField(blank=True, null=True, verbose_name="Ruedas")
    ejes = models.IntegerField(blank=True, null=True, verbose_name="Ejes")
    cilindros = models.IntegerField(blank=True, null=True, verbose_name="Cilindros")
    longitud = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Longitud (m)")
    altura = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Altura (m)")
    ancho = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Ancho (m)")
    cilindrada = models.CharField(max_length=50, blank=True, null=True, verbose_name="Cilindrada")
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="P.Bruto (Kg)")
    peso_neto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="P.Neto (Kg)")
    carga_util = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Carga Útil (Kg)")
    
    # Datos Registrales
    partida_registral = models.CharField(max_length=50, blank=True, null=True, verbose_name="Partida Registral")
    dua_dam = models.CharField(max_length=50, blank=True, null=True, verbose_name="DUA/DAM")
    titulo = models.CharField(max_length=50, blank=True, null=True, verbose_name="Título")
    fecha_titulo = models.DateField(blank=True, null=True, verbose_name="Fecha Título")

    horometro_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    odometro_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS_VEHICULO, default='DISPONIBLE')

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

class Repuesto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Parte")
    nombre = models.CharField(max_length=150, verbose_name="Nombre / Descripción")
    marca = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca del Repuesto")
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Ej: Filtros, Rodamientos, Eléctrico")
    unidad_medida = models.CharField(max_length=20, default='Unidad', help_text="Ej: Unidad, Litros, Galones, Metros")
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación en Almacén", help_text="Ej: Estante A1, Pasillo 3")
    stock = models.IntegerField(default=0, verbose_name="Stock Actual")
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock Mínimo de Alerta")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio Unitario (Aprox)")

    def __str__(self):
        return f"{self.codigo} - {self.nombre} (Stock: {self.stock})"

class OrdenTrabajo(models.Model):
    TIPOS_MANTENIMIENTO = [
        ('PREVENTIVO', 'Preventivo'),
        ('CORRECTIVO', 'Correctivo'),
    ]
    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    ESTADOS_ORDEN = [
        ('CREADA', 'Creada'),
        ('EN_PROCESO', 'En Proceso'),
        ('ESPERANDO_REPUESTO', 'Esperando Repuesto'),
        ('COMPLETADA', 'Completada'),
        ('REV_CONFIRMADA', 'Rev. Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    codigo = models.CharField(max_length=20, unique=True, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='ordenes')
    tipo_mantenimiento = models.CharField(max_length=20, choices=TIPOS_MANTENIMIENTO)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='MEDIA')
    descripcion = models.TextField(help_text="Descripción del problema o mantenimiento a realizar")
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_asignadas')
    estado = models.CharField(max_length=20, choices=ESTADOS_ORDEN, default='CREADA')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    
    # Datos reportados por el técnico
    horometro_registro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    odometro_registro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tiempo_trabajado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Horas trabajadas")
    reporte_trabajos = models.TextField(blank=True, null=True, help_text="Trabajos realizados por el técnico")

    def save(self, *args, **kwargs):
        if not self.codigo:
            import uuid
            self.codigo = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OT-{self.codigo} - {self.vehiculo.numero_economico}"

class ChecklistOrden(models.Model):
    orden = models.OneToOneField(OrdenTrabajo, on_delete=models.CASCADE, related_name='checklist')
    
    # 1. Niveles y Fluidos
    nivel_aceite_motor = models.BooleanField(default=False, verbose_name="Nivel de Aceite de Motor")
    nivel_refrigerante = models.BooleanField(default=False, verbose_name="Nivel de Refrigerante")
    nivel_aceite_hidraulico = models.BooleanField(default=False, verbose_name="Nivel de Aceite Hidráulico")
    nivel_aceite_transmision = models.BooleanField(default=False, verbose_name="Nivel de Aceite de Transmisión")
    fugas_visibles = models.BooleanField(default=False, verbose_name="Ausencia de Fugas (Aceite/Agua)")

    # 2. Seguridad y Cabina
    cinturon_seguridad = models.BooleanField(default=False, verbose_name="Cinturón de Seguridad")
    alarma_retroceso = models.BooleanField(default=False, verbose_name="Alarma de Retroceso")
    claxon = models.BooleanField(default=False, verbose_name="Claxon / Bocina")
    extintor_botiquin = models.BooleanField(default=False, verbose_name="Extintor y Botiquín")
    espejos_vidrios = models.BooleanField(default=False, verbose_name="Espejos y Parabrisas")
    limpiaparabrisas = models.BooleanField(default=False, verbose_name="Limpiaparabrisas")

    # 3. Sistema Eléctrico y Luces
    luces_delanteras = models.BooleanField(default=False, verbose_name="Luces Delanteras")
    luces_traseras_freno = models.BooleanField(default=False, verbose_name="Luces Traseras y de Freno")
    luces_direccionales = models.BooleanField(default=False, verbose_name="Luces Direccionales")
    circulina_baliza = models.BooleanField(default=False, verbose_name="Circulina / Baliza (Pirata)")
    bateria_cables = models.BooleanField(default=False, verbose_name="Batería y Bornes limpios")

    # 4. Estructura y Rodamiento
    neumaticos_presion = models.BooleanField(default=False, verbose_name="Presión de Neumáticos")
    neumaticos_desgaste = models.BooleanField(default=False, verbose_name="Desgaste/Cortes (Neumáticos u Orugas)")
    tuercas_pernos = models.BooleanField(default=False, verbose_name="Tuercas y Pernos Ajustados")
    estado_chasis_tolva = models.BooleanField(default=False, verbose_name="Estado de Chasis y Tolva")

    # 5. Sistema Operativo y Mandos
    freno_servicio_parqueo = models.BooleanField(default=False, verbose_name="Frenos (Servicio y Parqueo)")
    direccion = models.BooleanField(default=False, verbose_name="Sistema de Dirección")
    mandos_hidraulicos = models.BooleanField(default=False, verbose_name="Mandos Hidráulicos / Joysticks")
    tablero_indicadores = models.BooleanField(default=False, verbose_name="Tablero e Indicadores sin Alertas")

    observaciones = models.TextField(blank=True, null=True, help_text="Anotar cualquier anomalía encontrada en la inspección.")

    def __str__(self):
        return f"Checklist - {self.orden.codigo}"

class RepuestoOrden(models.Model):
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='repuestos_usados')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    precio_historico = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio al momento de usar el repuesto")

    def save(self, *args, **kwargs):
        if not self.pk: # Si es nuevo, copiamos el precio actual del repuesto
            self.precio_historico = self.repuesto.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.repuesto.nombre} - OT-{self.orden.codigo} ({self.cantidad})"

class MovimientoInventario(models.Model):
    TIPOS = [
        ('ENTRADA', 'Entrada (+)'),
        ('SALIDA', 'Salida (-)'),
        ('AJUSTE', 'Ajuste de Inventario'),
    ]
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=15, choices=TIPOS)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    origen_destino = models.CharField(max_length=150, help_text="Ej: Orden OT-123, Compra FACT-456, Ajuste Manual")
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} | {self.repuesto.nombre} | Cant: {self.cantidad}"

class Compra(models.Model):
    numero_factura = models.CharField(max_length=50, blank=True, null=True)
    proveedor = models.CharField(max_length=150)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    documento_adjunto = models.FileField(upload_to='compras/adjuntos/', null=True, blank=True, help_text="PDF o Imagen de la factura")
    fecha_compra = models.DateField()
    
    # Opcionales para trazabilidad
    vehiculo_destino = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    repuesto_abastecido = models.ForeignKey(Repuesto, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad_repuesto = models.IntegerField(null=True, blank=True, help_text="Si se compraron repuestos para inventario")

    def __str__(self):
        return f"Compra {self.numero_factura or 'S/N'} - {self.proveedor}"

class AlertaPreventiva(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='alertas')
    tipo_alerta = models.CharField(max_length=100, help_text="Ej: Cambio de Aceite, Mantenimiento 1000H")
    intervalo_horas = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Cada cuántas horas alertar")
    intervalo_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Cada cuántos km alertar")
    ultimo_horometro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Horómetro en el último mantenimiento")
    ultimo_odometro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Odómetro en el último mantenimiento")
    activa = models.BooleanField(default=True)

    def due_soon(self):
        if not self.activa:
            return False
        if self.intervalo_horas and self.ultimo_horometro is not None:
            if self.vehiculo.horometro_actual >= (self.ultimo_horometro + self.intervalo_horas - 50): # 50 horas de holgura
                return True
        if self.intervalo_km and self.ultimo_odometro is not None:
            if self.vehiculo.odometro_actual >= (self.ultimo_odometro + self.intervalo_km - 500): # 500 km de holgura
                return True
        return False

    def __str__(self):
        return f"Alerta {self.tipo_alerta} - {self.vehiculo.numero_economico}"
