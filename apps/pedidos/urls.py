from django.urls import path

from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.ver, name='ver'),
    path('agregar/<int:id>/', views.agregar, name='agregar'),
    path('restar/<int:id>/', views.restar, name='restar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('limpiar/', views.limpiar, name='limpiar'),
    path('checkout/', views.checkout_simulado, name='checkout'),
]
