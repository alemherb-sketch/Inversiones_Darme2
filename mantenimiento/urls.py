from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Desktop
    path('', views.dashboard, name='dashboard'),
    
    # Auth General
    path('logout/', views.custom_logout, name='logout'),
    
    # Vehiculos
    path('vehiculos/', views.vehiculo_lista, name='vehiculo_lista'),
    path('vehiculos/nuevo/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculos/<int:pk>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculos/editar/<int:pk>/', views.vehiculo_editar, name='vehiculo_editar'),
    path('vehiculos/eliminar/<int:pk>/', views.vehiculo_eliminar, name='vehiculo_eliminar'),
    
    # Ordenes
    path('ordenes/', views.orden_lista, name='orden_lista'),
    path('ordenes/nueva/', views.orden_crear, name='orden_crear'),
    path('ordenes/<int:pk>/', views.orden_detalle, name='orden_detalle'),
    path('ordenes/editar/<int:pk>/', views.orden_editar, name='orden_editar'),
    path('ordenes/eliminar/<int:pk>/', views.orden_eliminar, name='orden_eliminar'),
    
    # Compras
    path('compras/', views.compra_lista, name='compra_lista'),
    path('compras/nueva/', views.compra_crear, name='compra_crear'),
    path('compras/<int:pk>/', views.compra_detalle, name='compra_detalle'),
    path('compras/editar/<int:pk>/', views.compra_editar, name='compra_editar'),
    path('compras/eliminar/<int:pk>/', views.compra_eliminar, name='compra_eliminar'),

    # Logistica / Almacén
    path('logistica/', views.logistica_dashboard, name='logistica_dashboard'),
    path('logistica/kardex/', views.kardex_lista, name='kardex_lista'),
    path('logistica/movimiento-manual/', views.movimiento_manual, name='movimiento_manual'),

    # Repuestos (CRUD interno)
    path('repuestos/', views.repuesto_lista, name='repuesto_lista'),
    path('repuestos/nuevo/', views.repuesto_crear, name='repuesto_crear'),
    path('repuestos/<int:pk>/', views.repuesto_detalle, name='repuesto_detalle'),
    path('repuestos/editar/<int:pk>/', views.repuesto_editar, name='repuesto_editar'),
    path('repuestos/eliminar/<int:pk>/', views.repuesto_eliminar, name='repuesto_eliminar'),

    # Usuarios / Técnicos
    path('usuarios/', views.usuario_lista, name='usuario_lista'),
    path('usuarios/nuevo/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/editar/<int:pk>/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/eliminar/<int:pk>/', views.usuario_eliminar, name='usuario_eliminar'),
    
    # --- PORTAL MÓVIL (TÉCNICOS) ---
    path('mobile/login/', views.MobileLoginView.as_view(), name='mobile_login'),
    path('mobile/mis-ordenes/', views.mobile_mis_ordenes, name='mobile_mis_ordenes'),
    path('mobile/orden/<int:pk>/reportar/', views.mobile_reportar_orden, name='mobile_reportar_orden'),
]
