from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('gestion/', views.gestion, name='gestion'),
    path('crear/', views.crear, name='crear'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('gestion/eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('<slug:slug>/', views.detalle, name='detalle'),
]
