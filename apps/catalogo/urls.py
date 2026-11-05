from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('gestion/', views.gestion, name='gestion'),
    path('crear/', views.crear, name='crear'),
    path('<slug:slug>/', views.detalle, name='detalle'),
]
