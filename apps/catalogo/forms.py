from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'categoria', 'marca', 'contenido', 'descripcion',
            'precio', 'stock', 'estado', 'imagen', 'destacado', 'activo',
        ]
